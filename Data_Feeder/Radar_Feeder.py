#!/usr/bin/env python
# coding: utf-8
"""
module: data pipeline for radar processing
"""

import os
import re
import sys
import time
import warnings
import numpy as np
import pandas as pd

from .base import Gen_Feeder
from collections import defaultdict

__all__ = (
    'Corner_Radar_Points_Gen_Feeder',
    'Corner_Radar_Boxcenter_Gen_Feeder',
    'Back_Radar_Bbox_Gen_Feeder'
)


class Corner_Radar_Points_Gen_Feeder(Gen_Feeder):
    """
    read, parse & feed the radar csv & label yaml file 
    note: all info in radar csv is parsed as float
    """
    def __init__(self, data_dir, class_num=2, class_name=['other', 'car'], select_cols=None, header=True, split=None,
                 file_re='.*\.csv', line_re='\t (?!3).*', use_onehot=True, sort_cols=True):
        super(Corner_Radar_Points_Gen_Feeder, self).__init__(data_dir, class_num, class_name, file_re, use_onehot, split)
        sys.path.append(os.path.join(data_dir, 'scripts'))
        self.ext_module['radar_objects'] = __import__('radar_objects', fromlist=[''])
        self.ext_module['yaml'] = __import__('yaml', fromlist=[''])
        self.dataset_name = 'corner'
        self.header = header

        if select_cols is not None and sort_cols:
            self.select_cols = sorted(select_cols, reverse=False) # ascending order
        else:
            self.select_cols = select_cols

        self.line_re = line_re
        self.select_lines = lambda lines: filter(lambda x: re.fullmatch(self.line_re, x), lines)

        # get feature name from header
        if header == True:
            self.feature_names = self._probe_feature_name()

    def _probe_feature_name(self):
        for path in self.traverser.traverse_file_path():
            with open(path, 'r') as file:
                feature_names = file.readline().strip().split(',')
            if self.select_cols is not None:
                feature_names = [feature_names[idx] for idx in self.select_cols]
            return feature_names

    def _get_input(self, dirpath, name):
        with open(os.path.join(dirpath, name), 'r') as file:
            if self.header:
                file.readline()
            all_lines = file.read().strip('\n').split('\n')
        
        input_arr = np.array([[float(elem) for elem in row.strip().split(',')] for row in self.select_lines(all_lines) if row])
        if input_arr.size > 0:
            id_pair_arr = input_arr[:, [0, 1]]
        else:
            id_pair_arr = np.array([])

        return id_pair_arr, input_arr

    def _get_label_path_given_input(self, input_dir, input_name):
        label_dir = input_dir.rstrip('/').rstrip('radar_file') + 'result/'
        label_file = input_name.rstrip('csv') + 'yaml'
        return os.path.join(label_dir, label_file)

    def _get_car_point_id_arr(self, path):
        with open(path, 'r') as yaml_file:
            # not safe: consider safe_load (for untrusted source) / load_all (for multiple yaml obj)
            yaml_struct = self.ext_module['yaml'].load(yaml_file)

        if yaml_struct == None:
            raise Warning(path + ' is empty')

        # get the radar point annotated as car (in the bounding box)
        id_list = []
        for result in yaml_struct:
            id_list.extend([[point.group_id, point.target_id] for point in result.lists])
        
        return np.array(id_list, dtype=int)

    def _get_label_given_input_id_arr(self, input_dir, input_name, input_id_arr):
        path = self._get_label_path_given_input(input_dir, input_name) # path for corresponding yaml file
        id_arr = self._get_car_point_id_arr(path) # id pair for points labeled as car

        label_arr = np.zeros(input_id_arr.shape[0], dtype=int)
        for id_pair in id_arr:
            # get the idx in the array for matched (group & target id)
            idx_list = np.where((id_pair == input_id_arr).all(axis=-1))[0] # 1-D idx
            if len(idx_list) > 0:
                idx = int(idx_list[0]) # get the first one if multiple found
                label_arr[idx] = 1
        
        if self.use_onehot:
            label_arr = self._to_onehot(label_arr)
        return label_arr

    def _get_input_label_pair(self, dirpath, name):
        cur_id_arr, cur_input = self._get_input(dirpath, name)
        cur_label = self._get_label_given_input_id_arr(dirpath, name, cur_id_arr)

        if self.select_cols is not None and len(cur_input) > 0:
            cur_input = cur_input[:, self.select_cols]
        yield [cur_input, cur_label]

    def _record_pred(self, data_dirpath, data_name, pred_func, model_name, out_subdir, overwrite):
        cur_id_arr, cur_input = self._get_input(data_dirpath, data_name)
        if self.select_cols is not None:
            cur_input = cur_input[:, self.select_cols]
        cur_pred = pred_func(cur_input)
        if self.use_onehot:
            cur_pred = cur_pred[:,1] # get the pred prob for car

        if data_name in os.listdir(out_subdir) and not overwrite:  # previous pred existed
            df = pd.read_csv(os.path.join(out_subdir, data_name), index_col=['group_id', 'target_id'])
            if (np.array(df.index.tolist()) == cur_id_arr).all():  # id arr consistent
                df[model_name] = cur_pred
            else: # inconsistent
                warnings.warn('feeder\'s id arr != previously saved pred\'s id arr, try merging...')
                print('debug info:')
                print(df.head(10))
                print(cur_id_arr[:10,:])
                print(np.array(df.index.labels).T[:10,:])
                print(np.array(df.index.tolist())[:10])
                print(data_dirpath, data_name)
                idx = pd.MultiIndex.from_arrays(cur_id_arr.T, names=['group_id', 'target_id'])  # construct idx
                new_df = pd.DataFrame(cur_pred, columns=[model_name], index=idx)
                print(new_df.head(10))
                raise Exception('merge failed - not supported yet')

        else:  # first pred || overwrite anyway
            idx = pd.MultiIndex.from_arrays(cur_id_arr.T, names=['group_id', 'target_id']) # construct idx
            df = pd.DataFrame(cur_pred, columns=[model_name], index=idx)
        df.to_csv(os.path.join(out_subdir, data_name))
    
    def load_with_metadata(self, data_dir, data_name, pred_dir):
        """
        load data in one file into a list of dict with corresponding prediction, input & picture
        """
        mpimg = __import__('matplotlib.image', fromlist=[''])
        # get input, xy, label pair
        cur_id_arr, cur_input = self._get_input(data_dir, data_name)
        xy_arr = cur_input[:, [3, 2]] # xy_arr
        xy_arr[:, 0] = -xy_arr[:, 0]
        if self.select_cols is not None: # selected input
            cur_input = cur_input[:, self.select_cols]
        cur_label = self._get_label_given_input_id_arr(data_dir, data_name, cur_id_arr) # label

        dir_list = data_dir.strip('/').split('/')
        subdir = '/'.join(dir_list[dir_list.index(self.dataset_name) + 1:])

        # load pred
        pred_path = os.path.join(pred_dir, subdir, data_name)
        df = pd.read_csv(pred_path, index_col=['group_id', 'target_id'])
        assert (np.array([[n for n in row] for row in df.index]) == cur_id_arr).all()  # ensure in the same order
        cur_pred = {}
        for k in df.columns:
            if 'sk' in k:
                cur_pred[k] = np.array(df[k])
        # load pic
        pic_path = os.path.join(data_dir.replace('radar_file', 'image_file'), data_name.replace('.csv', '.jpg'))
        cur_pic = mpimg.imread(pic_path)

        return [{'input': cur_input, 'input_xy': xy_arr, 'label': cur_label, 'pred': cur_pred, 'img': cur_pic}]

    def iterate_with_metadata(self, pred_dir):
        """
        iterate data example with their metadata (prediction & image)
        """
        for dir_path, fname in self.traverser.traverse_file():
            yield self.load_with_metadata(dir_path, fname, pred_dir)[0]


class Corner_Radar_Boxcenter_Gen_Feeder(Gen_Feeder):
    """
    read, parse & feed the radar csv & label (box center) yaml file
    note: voxelization for object localization
    """
    def __init__(self, data_dir, select_cols, class_num=2, class_name=['n', 'c'], focus_size=(15, 20), resolution=0.5,
                 header=True, file_re='.*\.csv', line_re='\t (?!3).*', split=None, weight_type='', norm_type=''):
        super(Corner_Radar_Boxcenter_Gen_Feeder, self).__init__(data_dir, class_num, class_name, file_re, use_onehot=True, split=split)
        sys.path.append(os.path.join(data_dir, 'scripts'))
        self.ext_module['radar_objects'] = __import__('radar_objects', fromlist=[''])
        self.ext_module['yaml'] = __import__('yaml', fromlist=[''])
        self.dataset_name = 'corner'
        self.header = header

        self.line_re = line_re
        self.select_cols = sorted(select_cols, reverse=False) # ascending order
        self.select_lines = lambda lines: filter(lambda x: re.fullmatch(self.line_re, x), lines)

        # get feature name from header
        if header == True:
            self.feature_names = self._probe_feature_name()

        self.focus_size = focus_size
        self.resolution = resolution
        self.focus_index = np.around([2 * i / resolution for i in focus_size]).astype(int)

        self.img_size = [int(i * 2 / resolution) for i in focus_size]  # width, height - in cartesian coord
        self.input_shape = self.img_size.copy()
        self.input_shape.append(len(self.select_cols))  # append channel num
        self.label_shape = self.img_size.copy()
        self.label_shape.append(2)

        self.weight_type = weight_type
        assert weight_type in ['', 'bal']
        self._cal_weight()
        
        self.norm_type = norm_type
        assert norm_type in ['', 'm', 's']
        self._cal_norm()        

    def _probe_feature_name(self):
        for path in self.traverser.traverse_file_path():
            with open(path, 'r') as file:
                feature_names = file.readline().strip().split(',')
            if self.select_cols is not None:
                feature_names = [feature_names[idx] for idx in self.select_cols]
            return feature_names

    def _cal_norm(self):
        def _cal_mean():
            input_sum = 0
            input_cnt = 0
            for cur_input, _ in self.iterate_data():
                input_sum = input_sum + cur_input
                input_cnt += 1
            return (input_sum / input_cnt).mean(axis=(0, 1))  # mean for each channel
        def _cal_std(input_mean):
            input_sum = 0
            input_cnt = 0
            for cur_input, _ in self.iterate_data():
                input_sum = input_sum + (cur_input - input_mean) ** 2
                input_cnt += 1
            return (input_sum / input_cnt).mean(axis=(0, 1))  # std for each channel

        def _cal_norm_params():
            norm_params = dict()
            if self.norm_type:
                norm_params['mean'] = _cal_mean()
                if self.norm_type in ['s']:  # require std: standardizing
                    norm_params['std'] = _cal_std(norm_params['mean'])
            return norm_params

        self.norm_params = []
        if self.split is not None:
            self.norm_params = []
            for split_n in range(len(self.path_split)): # for each data split
                self.switch_split(split_n)
                self.norm_params.append(_cal_norm_params())
            self.switch_split(0)
        else:
            self.norm_params = _cal_norm_params()

    def _fill_image(self, xy_arr, feature_arr, img):
        """
        in-place fill image with clipping
        """
        xy_arr = np.around((xy_arr + self.focus_size) / self.resolution).astype(int)  # round (already in cartesian coord)
        infocus_idx = np.where(np.logical_and(0 <= xy_arr, xy_arr < self.focus_index).all(axis=1))  # assure in focus
        img[xy_arr[infocus_idx, 0], xy_arr[infocus_idx, 1]] = feature_arr[infocus_idx]  # direct mapping - x as row, y as col
        return img

    def _get_input(self, dirpath, name):
        with open(os.path.join(dirpath, name), 'r') as file:
            if self.header:
                file.readline()
            all_lines = file.read().strip('\n').split('\n')
        
        input_arr = np.array([[float(elem) for elem in row.strip().split(',')] for row in self.select_lines(all_lines)])

        cur_input = np.zeros(shape=self.input_shape, dtype=float)
        if input_arr.size > 0:
            # use cartesian coord
            xy_arr = input_arr[:, [3, 2]]
            xy_arr[:, 0] = -xy_arr[:, 0]
            feature_arr = input_arr[:, self.select_cols]
            cur_input = self._fill_image(xy_arr=xy_arr, feature_arr=feature_arr, img=cur_input)

        return cur_input

    def _get_label_path_given_input(self, input_dir, input_name):
        label_dir = input_dir.rstrip('/').rstrip('radar_file') + 'result/'
        label_file = input_name.rstrip('csv') + 'yaml'
        return os.path.join(label_dir, label_file)

    def _get_box_center_mask(self, path):
        with open(path, 'r') as yaml_file:
            # not safe: consider safe_load (for untrusted source) / load_all (for multiple yaml obj)
            yaml_struct = self.ext_module['yaml'].load(yaml_file)

        if yaml_struct == None:
            raise Warning(path + ' is empty')

        # get the radar point annotated as car (in the bounding box)
        center_list = []
        for result in yaml_struct:
            # use cartesian coord (label plt is NOT in cartesian coord)
            center = [-result.position.y - result.size.y / 2, result.position.x + result.size.x / 2]
            center_list.append(center)

        cur_label = np.zeros(self.label_shape, dtype=int)
        cur_label[..., 0] = 1 # assign 1 to [0] of last dimension (non-car)
        if len(center_list) > 0:
            label_arr = self._to_onehot([1] * len(center_list))
            cur_label = self._fill_image(xy_arr=np.array(center_list), feature_arr=label_arr, img=cur_label)
        return cur_label

    def _get_input_label_pair(self, dirpath, name):
        cur_input = self._get_input(dirpath, name)
        yaml_path = self._get_label_path_given_input(dirpath, name) # path for corresponding yaml file
        cur_label = self._get_box_center_mask(yaml_path)
        yield [cur_input, cur_label]

    def record_prediction(self, pred_func, model_name, output_dir='./Prediction', dataset_name='Data', overwrite=False, options={'pred_type': 'csv',
                                                                                                                                 'protobuf_path': '../../Data/corner/evaluate-test',
                                                                                                                                 'proto_post': '.prototxt'}):
        """
        extended to accomodate protobuf
        """
        self.pred_opt = options
        pred_type = options['pred_type']
        if pred_type == 'protobuf':
            self._write_pred_to_file = self._write_pred_to_protobuf
            sys.path.append(options['protobuf_path'])
            self.pred_opt['rsds_data_pb2'] = __import__('rsds_data_pb2', fromlist=[''])
            self.pred_opt['proto_post'] = options['proto_post']
        else: # default to csv
            self._write_pred_to_file = self._write_pred_to_csv

        return Gen_Feeder.record_prediction(self, pred_func, model_name,
                                            output_dir=output_dir,
                                            dataset_name=dataset_name,
                                            overwrite=overwrite)

    def _record_pred(self, data_dirpath, data_name, pred_func, model_name, out_subdir, overwrite):
        cur_input = self._get_input(data_dirpath, data_name)
        cur_pred = pred_func(cur_input)[0] # assume 1 img per batch

        pred_center_list = []
        for x, y in zip(*np.where(cur_pred[..., 1] > cur_pred[..., 0])):  # becaues direct mapping when filling
            cart_xy = [coord * self.resolution - fc_size for coord, fc_size in zip([x, y], self.focus_size)]
            pred_center_list.append(cart_xy)  # cartesian coord cooresponding to car

        self._write_pred_to_file(pred_center_list, model_name, data_name, out_subdir, overwrite)
    
    def _write_pred_to_protobuf(self, pred_center_list, model_name, data_name, out_subdir, overwrite):
        default_size = self.resolution
        assert overwrite

        rst = self.pred_opt['rsds_data_pb2'].RsdsResults()
        for [cart_x, cart_y] in pred_center_list:
            t = rst.targets.add()
            # invalide value for required fields
            t.group_id = -1 
            t.track_id = -1
            # fill according to test_rsds.py, test plt & protobuf coord is NOT in cartesian coord)
            t.coord_x = cart_y
            t.coord_y = -cart_x
            t.size_x = default_size
            t.size_y = default_size
        with open(os.path.join(out_subdir, data_name.replace('.csv', self.pred_opt['proto_post'])), 'wb') as f:
            f.write(rst.SerializeToString())
        return

    def _write_pred_to_csv(self, pred_center_list, model_name, data_name, out_subdir, overwrite):
        if data_name in os.listdir(out_subdir) and not overwrite:  # previous pred existed
            df = pd.read_csv(os.path.join(out_subdir, data_name))
            df[model_name] = pred_center_list

        else:  # first pred || overwrite anyway
            df = pd.DataFrame(pred_center_list, columns=[model_name])
        df.to_csv(os.path.join(out_subdir, data_name), index=False)
    
    def load_with_metadata(self, data_dir, data_name, pred_dir):
        """
        load data in one file with corresponding prediction & picture
        """
        # get input & label pair
        cur_input = self._get_input(data_dir, data_name)
        yaml_path = self._get_label_path_given_input(data_dir, data_name) # path for corresponding yaml file
        cur_label = self._get_box_center_mask(yaml_path)

        dir_list = data_dir.strip('/').split('/')
        subdir = '/'.join(dir_list[dir_list.index(self.dataset_name) + 1:])

        # load pred
        pred_path = os.path.join(pred_dir, subdir, data_name)
        df = pd.read_csv(pred_path)
        cur_pred = {}
        for k in df.columns:
            if 'tf-fcnpipe' in k:
                cur_pred[k] = np.array([[int(i) for i in center_str.split('-')] for center_str in df[k]])

        # load pic
        pic_path = os.path.join(data_dir.replace('radar_file', 'image_file'), data_name.replace('.csv', '.jpg'))
        cur_pic = mpimg.imread(pic_path)
        return {'input': cur_input, 'label': cur_label, 'pred': cur_pred, 'img': cur_pic}


class Back_Radar_Bbox_Gen_Feeder(Gen_Feeder):
    """
    read, parse & feed the back radar data from proto (label) and txt (pred output) file
    """
    def __init__(self, data_dir, class_num=1, class_name=['car'], re_expr='.*\.prototxt', use_onehot=True, split=None,
                 weight_type='', norm_type='', resolution=0.5, label_type='protobuf', pred_type='txt',
                 config={'ext_module':{}, 'offset':{'pred':0, 'label':0}, 'skip':''}):
        super(Back_Radar_Bbox_Gen_Feeder, self).__init__(data_dir, class_num, class_name, re_expr=re_expr, use_onehot=use_onehot,
                                                         split=split, weight_type=weight_type, norm_type=norm_type)
        self.feature_names = []
        self.resolution = resolution # smallest unit for width, height & any comparance
        self.config = config

        assert label_type in ['protobuf']
        if label_type == 'protobuf':
            self._parse_label_file = self._parse_proto_label_file
        self.label_type = label_type

        assert pred_type in ['txt']
        self.pred_type = pred_type

        if 'ext_module' in self.config:
            for md_name in self.config['ext_module']:
                md_path = os.path.expanduser(self.config['ext_module'][md_name])
                sys.path.append(md_path)
                self.config['ext_module'][md_name] = __import__(md_name, fromlist=[''])
        
        if 'skip' in self.config:
            if self.config['skip']:
                self.config['skip'] = [[int(i) for i in rg.split('-')] for rg in self.config['skip'].split('|')]
            else:
                self.config.pop('skip', None)  # delete exclude time
        
    def _parse_input_file(self, dirpath, name):
        return iter(int, 1)  # infinite iterator

    @staticmethod
    def _rotate_coord_anticloclwise(x, y, theta):
        return y * np.sin(theta) + x * np.cos(theta), y * np.cos(theta) + x * np.sin(theta)

    @staticmethod
    def _transfer_coord(x, y, group_id):
        if group_id == 3:  # rear
            yaw = 3.13
            offset = [-3.95, 0]
            cartx, carty = Back_Radar_Bbox_Gen_Feeder._rotate_coord_anticloclwise(-y, x, -yaw)
        elif group_id == 4:  # rear-left
            yaw = 1.9736252
            offset = [-3.755, 0.775]
            cartx, carty = Back_Radar_Bbox_Gen_Feeder._rotate_coord_anticloclwise(y, x, -yaw)
        elif group_id == 5:  # rear-right
            yaw = -1.90517
            offset = [-3.955, -0.77]
            cartx, carty = Back_Radar_Bbox_Gen_Feeder._rotate_coord_anticloclwise(-y, x, -yaw)
        elif group_id == 2:  # front-right
            yaw = -0.929515
            offset = [0.615, -0.835]
            cartx, carty = Back_Radar_Bbox_Gen_Feeder._rotate_coord_anticloclwise(y, x, -yaw)
        elif group_id == 1:  # front-left
            yaw =  0.927957
            offset = [0.63, 0.84]
            cartx, carty = Back_Radar_Bbox_Gen_Feeder._rotate_coord_anticloclwise(-y, x, -yaw)
        elif group_id == 0:  # front
            yaw = 0.00812
            offset = [0.927, -0.16]
            cartx, carty = Back_Radar_Bbox_Gen_Feeder._rotate_coord_anticloclwise(-y, x, -yaw)
        else:
            raise NotImplementedError('not supported group_id %d' % group_id)
        return cartx - offset[1], carty + offset[0] # cartx = -y, carty = x

    def _parse_proto_label_box(self, pb_obstacle):
        # box central point
        box_cartx = -pb_obstacle.coordinate_radar.y
        box_carty = pb_obstacle.coordinate_radar.x

        elem = []
        cartx_list = []
        carty_list = []
        for t in pb_obstacle.targets:
            # radar point xy
            cart_xy = self._transfer_coord(t.coordinate.x, t.coordinate.y, t.group_id)
            elem.append((*cart_xy, -t.velocity.y, t.velocity.x, t.rcs))
            cartx_list.append(cart_xy[0])
            carty_list.append(cart_xy[1])

        if elem:
            points_w = max(cartx_list) - min(cartx_list)
            points_h = max(carty_list) - min(carty_list)
        else:
            points_w = 0
            points_h = 0

        # width, height (according to pb specification)
        w = max(self.resolution, points_w, pb_obstacle.object_size.y)
        h = max(self.resolution, points_h, pb_obstacle.object_size.x)
        # print('%.2f\t%.2f\t%.2f' % (self.resolution, points_w, pb_obstacle.object_size.y))
        # print('%.2f\t%.2f\t%.2f\t' % (self.resolution, points_h, pb_obstacle.object_size.x))
        # print('------------------')
        try:
            blockage = t.cover_rate
        except:
            blockage = 0
        
        return {'xy': (box_cartx - w / 2, box_carty - h / 2), 'width': w, 'height': h,
                'prob': [1], 'elem': elem, 'blockage': blockage}

    def _parse_proto_labelframe(self, label_frame):
        bbox_deflist = []
        for ob in label_frame.obstacles:
            bbox_def = self._parse_proto_label_box(ob)
            bbox_deflist.append(bbox_def)
        return [int(label_frame.timestamp * 1e6), bbox_deflist] # [time, [bbox_def]]
        
    def _parse_proto_label_file(self, dirpath, name):
        with open(os.path.join(dirpath, name), 'rb') as f:
            ptxt_bt = f.read()
        rst = self.config['ext_module']['radar_label_pb2'].LabelResultData()
        try:
            protobuf.text_format.Merge(ptxt_bt, rst)  # read from non-python
        except:
            rst.ParseFromString(ptxt_bt)  # read from python

        # generator for [time, points, [bbox def]]
        label_gen = (self._parse_proto_labelframe(frame) for frame in rst.label_data)
        if 'offset' in self.config and 'label' in self.config['offset']:
            for _ in range(self.config['offset']['label']):
                next(label_gen)
        return label_gen

    def _parse_pred_bbox(self, line, input_points=[]):
        # obstacle id, time_stamp, pos_x, pos_y, width, length, heading, vel_x, vel_y
        # vel => velocity, pos => central position under car coord
        line = line.split()
        cart_x = -float(line[3])
        cart_y = float(line[2])
        w = max(self.resolution, float(line[4]))
        h = max(self.resolution, float(line[5]))
        elem = [p for p in input_points if p[0] > cart_x and p[1] > cart_y and p[0] < cart_x + w and p[1] < cart_y + h]  # all points in box
        return {'xy': (cart_x - w / 2, cart_y - h / 2), 'width': w, 'height': h, 'prob': [1], 'elem': elem}

    def _parse_pred_lines(self, lines, input_points=[], label_time=-1):
        cur_time = int(lines[0])  # time stamp
        pred_bboxlist = [self._parse_pred_bbox(line, input_points) for line in lines[1:]]  # 0-1-more bbox def
        return cur_time, pred_bboxlist

    def _get_pred_name(self, name):
        return name.split('.')[0] + '.' + self.pred_type

    def _parse_pred_file_to_segment(self, dirpath, name):
        with open(os.path.join(dirpath, self._get_pred_name(name)), 'r') as f:
            exp_list = f.read().strip('\n').split('\n\n')
        seg_gen = (exp.split('\n') for exp in exp_list)

        if 'offset' in self.config and 'pred' in self.config['offset']:
            for i in range(self.config['offset']['pred']):
                next(seg_gen)
        return seg_gen

    def _get_input_label_pair(self, dirpath, name):
        raise NotImplementedError

    def _iter_with_metadata_given_file(self, data_dir, data_name, pred_dir):
        input_gen = self._parse_input_file(data_dir, data_name)
        label_gen = self._parse_label_file(data_dir, data_name)
        predseg_gen = self._parse_pred_file_to_segment(pred_dir, data_name)

        for cur_input, cur_label in zip(input_gen, label_gen):
            label_time = cur_label[0]
            label_bboxlist = cur_label[-1]

            cur_input = list(set(sum([bbox['elem'] for bbox in label_bboxlist], [])))
            input_xy = np.array([[point[0],point[1]] for point in cur_input])

            pred_lines = next(predseg_gen)
            pred_time, pred_bboxlist = self._parse_pred_lines(pred_lines, input_points=cur_input)

            if 'skip' in self.config:
                for rg in self.config['skip']:
                    while rg[0] <= pred_time and pred_time <= rg[1]:  # skip through current exclude range
                        print('skip ', pred_time)
                        pred_lines = next(predseg_gen)
                        pred_time, pred_bboxlist = self._parse_pred_lines(pred_lines, input_points=[])

            # fix pred to find corresponding label (especially after skip)
            while label_time < pred_time:
                cur_input = next(input_gen)
                cur_label = next(label_gen)
                label_time = cur_label[0]
                label_bboxlist = cur_label[-1]

                cur_input = list(set(sum([bbox['elem'] for bbox in label_bboxlist], [])))
                input_xy = np.array([[point[0],point[1]] for point in cur_input])
                _, pred_bboxlist = self._parse_pred_lines(pred_lines, input_points=cur_input)

            assert pred_time == label_time

            yield {'input': cur_input, 'input_xy': input_xy, 'label': label_bboxlist, 'pred': pred_bboxlist, 'time_stamp': pred_time}

    def iterate_with_metadata(self, pred_dir):
        """
        iterate data example with aligned recorded prediction
        """
        for dirpath, name in self.traverser.traverse_file():
            yield from self._iter_with_metadata_given_file(dirpath, name, pred_dir)

    def load_with_metadata(self, data_dir, data_name, pred_dir):
        """
        load data in one file into a list of dict with corresponding prediction & input
        """
        return [data_dict for data_dict in self._iter_with_metadata_given_file(data_dir, data_name, pred_dir)]
