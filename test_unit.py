#!/usr/bin/env python3
# 06/25/2021
# Dev: Cody Yarger
# Assignment 09 - Advanced Language Constructs


'''
    Test unit for social netowrk
'''
# pylint: disable=C0103
# pylint: disable=W0212
# pylint: disable=R0904


from unittest import TestCase
import os
import shutil
from loguru import logger
import peewee as pw
from playhouse.dataset import DataSet
import users
import user_status
import list_user_images


class UserDatabaseTest(TestCase):
    '''
        Tests for UserCollection methods
    '''
###############################################################################
# setUp and tearDown
###############################################################################

    def setUp(self):
        ''' Setup test database '''

        # instantiate database
        self.db = DataSet('sqlite:///:memory:')

        # ===========================================================================
        self.user_collection = self.db['Users']
        self.user_collection.insert(user_id='dummy',
                                    user_name='dummy',
                                    user_last_name='dummy',
                                    email='dummy'
                                    )
        self.user_collection.create_index(['user_id'], unique=True)
        self.user_collection.delete(user_id='dummy',
                                    user_name='dummy',
                                    user_last_name='dummy',
                                    email='dummy')

        # ===========================================================================
        self.status_collection = self.db['Status']
        self.status_collection.insert(status_id='dummy',
                                      user_id='dummy',
                                      status_text='dummy')

        self.status_collection.create_index(['status_id'], unique=True)
        self.status_collection.delete(status_id='dummy',
                                      user_id='dummy',
                                      status_text='dummy')

        # ===========================================================================
        self.image_collection = self.db['Picture']
        self.image_collection.insert(picture_id='dummy',
                                     user_id='dummy',
                                     tags='dummy')

        self.image_collection.create_index(['picture_id'], unique=True)
        self.image_collection.delete(picture_id='dummy',
                                     user_id='dummy',
                                     tags='dummy')
        # =======================================================================
        # Test user table data
        users_list = [('id1', 'email1', 'name1', 'last1'),
                      ('id2', 'email2', 'name2', 'last2'),
                      ('id3', 'email3', 'name3', 'last3'),
                      ('id4', 'email4', 'name4', 'last4')]

        # for users populate test database
        for user in users_list:
            # insert user data into db model
            try:
                self.user_collection.insert(user_id=user[0],
                                            user_name=user[1],
                                            user_last_name=user[2],
                                            email=user[3])
            except pw.IntegrityError:
                logger.info('Error populating user_collection')

        # =======================================================================
        # Test status table data
        statuses = [('id1', 'status1', 'text1'),
                    ('id2', 'ststus2', 'text2'),
                    ('id3', 'ststus3', 'text3')]

        # for status populate test database
        for status in statuses:
            try:
                self.status_collection.insert(user_id=status[0],
                                              status_id=status[1],
                                              status_text=status[2])
            except pw.IntegrityError:
                logger.info('Error populating status_collection')

        # =======================================================================
        # Test Picture table data
        images = [('id1', '000001.png', '#home'),
                  ('id2', '000002.png', '#home #trips'),
                  ('id3', '000003.png', '#home #trips #oregon'),
                  ('id4', '000004.png', '#home #trips #oregon'),
                  ('test_id1', '000005.png', '#test_dir1')]

        # for images populate test database
        for image in images:
            try:
                self.image_collection.insert(user_id=image[0],
                                             picture_id=image[1],
                                             tags=image[2])
            except pw.IntegrityError:
                logger.info('Error populating image_collection')

        # generate test directory and .png file for disc storage tests
        cwd = os.getcwd()
        test_path_1 = os.path.join(cwd, 'test_id1', 'test_dir1')
        os.makedirs(test_path_1)
        if os.path.isdir(test_path_1):
            f = open(test_path_1 + '/' + '000005.png', 'wb')
            f.write('-'.encode())
            f.close()

        cwd = os.getcwd()
        test_path_2 = os.path.join(cwd, 'test_id2', 'test_dir2')
        os.makedirs(test_path_2)
        if os.path.isdir(test_path_2):
            f = open(test_path_2 + '/' + '000006.png', 'wb')
            f.write('-'.encode())
            f.close()

    def tearDown(self):
        ''' Teardown test database and remove image files and directories '''
        self.db.close()

        # teardown test directories and files
        ids = ['id1', 'id2', 'id3', 'id4', 'test_id1', 'test_id2']
        cwd = os.getcwd()
        for userid in ids:
            images_path = os.path.join(cwd, userid)
            if os.path.exists(images_path):
                shutil.rmtree(images_path)

###############################################################################
# users.py tests
###############################################################################
    # @pysnooper.snoop()
    def test_add_user(self):
        ''' Test add user '''
        expected = users.add_user('id5', 'name5', 'last5', 'email5', self.user_collection)
        self.assertTrue(expected)

    def test_add_user_false(self):
        ''' Test add user false'''
        expected = users.add_user('id1', 'name4', 'last4', 'email4', self.user_collection)
        self.assertFalse(expected)

    def test_add_user_len_false(self):
        ''' Test add user false'''
        thirty = "x"*31
        expected = users.add_user(thirty, 'name4', 'last4', 'email4', self.user_collection)
        self.assertFalse(expected)

    def test_modify_user(self):
        '''Test modify user'''
        expected = users.modify_user('id1', 'namex', 'lastx', 'emailx', self.user_collection)
        self.assertTrue(expected)

    def test_modify_user_false(self):
        ''' Test modify user false'''
        expected = users.modify_user('idx', 'namex', 'lastx', 'emailx', self.user_collection)
        self.assertFalse(expected)

    def test_modify_user_len_false(self):
        ''' Test modify user false'''
        thirty = "x"*31
        expected = users.modify_user('idx', thirty, 'lastx', 'emailx', self.user_collection)
        self.assertFalse(expected)

    def test_delete_user(self):
        '''Test delete user'''
        expected = users.delete_user('id1', self.user_collection, self.status_collection)
        self.assertTrue(expected)

    def test_delete_user_false(self):
        ''' Test delete user false'''
        expected = users.delete_user('idx', self.user_collection, self.status_collection)
        self.assertFalse(expected)

    def test_search_user(self):
        '''Test search user'''
        expected = users.search_user('id1', self.user_collection)
        self.assertTrue(expected)

    def test_search_user_false(self):
        ''' Test search user false'''
        expected = users.search_user('idx', self.user_collection)
        self.assertFalse(expected)


# ###############################################################################
# # user_status.py tests
# ###############################################################################

    def test_add_status(self):
        '''Test add status'''
        expected = user_status.add_status('id1',
                                          'statusx',
                                          'text1',
                                          self.status_collection,
                                          self.user_collection)
        self.assertTrue(expected)

    def test_add_status_false(self):
        ''' Test add status false'''
        expected = user_status.add_status('idx',
                                          'status1',
                                          'text1',
                                          self.status_collection,
                                          self.user_collection)
        self.assertFalse(expected)

    def test_modify_status(self):
        '''Test modify status'''
        expected = user_status.modify_status('status1',
                                             'new_text',
                                             self.status_collection)
        self.assertTrue(expected)

    def test_modify_status_false(self):
        ''' Test modify status false'''
        expected = user_status.modify_status('statusx',
                                             'text1',
                                             self.status_collection)
        self.assertFalse(expected)

    def test_delete_status(self):
        '''Test delete status'''
        expected = user_status.delete_status('status1', self.status_collection)
        self.assertTrue(expected)

    def test_delete_status_false(self):
        ''' Test delete status false'''
        expected = user_status.delete_status('statusx', self.status_collection)
        self.assertFalse(expected)

    def test_search_status(self):
        '''Test search status'''
        expected = user_status.search_status('status1', self.status_collection)
        self.assertTrue(expected)

    def test_search_status_false(self):
        ''' Test search status false'''
        expected = user_status.search_status('statusx', self.status_collection)
        self.assertFalse(expected)

###############################################################################
# list_user_images.py tests
###############################################################################

    def test_add_image(self):
        ''' Test add images '''
        expected = list_user_images.add_image('id1',
                                              '#tag',
                                              self.user_collection,
                                              self.image_collection)
        self.assertTrue(expected)

    def test_add_image_badtag(self):
        ''' Test add images missing hash '''
        expected = list_user_images.add_image('id1',
                                              '#tag badtag',
                                              self.user_collection,
                                              self.image_collection)
        self.assertFalse(expected)

    def test_add_image_extra_spaces(self):
        ''' Test add images extra spaces'''
        expected = list_user_images.add_image('id2',
                                              '#tag    #badtag2',
                                              self.user_collection,
                                              self.image_collection)
        self.assertTrue(expected)

    def test_add_image_no_records(self):
        ''' Test add images '''

        images = ['000001.png', '000002.png', '000003.png']
        for picid in images:
            self.image_collection.delete(picture_id=picid)

        expected = list_user_images.add_image('id2',
                                              '#tag',
                                              self.user_collection,
                                              self.image_collection)
        self.assertTrue(expected)

    def test_add_image_false(self):
        ''' Test add images '''
        expected = list_user_images.add_image('idx',
                                              '#tag',
                                              self.user_collection,
                                              self.image_collection)
        self.assertFalse(expected)

    def test_add_image_len_false(self):
        ''' Test add images '''
        tag = 'x'*101
        expected = list_user_images.add_image('idx',
                                              tag,
                                              self.user_collection,
                                              self.image_collection)
        self.assertFalse(expected)

    def test_load_image(self):
        ''' Test _load_image integrity error '''
        expected = list_user_images._load_image('id1',
                                                '000001.png',
                                                '#tag',
                                                self.image_collection)
        self.assertFalse(expected)

    def test_save_image_has_dir(self):
        ''' Test _save_image existing directory '''
        cwd = os.getcwd()
        images_path = os.path.join(cwd, 'id1', 'test')
        os.makedirs(images_path)
        expected = list_user_images._save_image('id1',
                                                '000004.png',
                                                '#test')
        self.assertTrue(expected)

    def test_save_image_no_dir(self):
        ''' Test _save_image no existing directory '''
        expected = list_user_images._save_image('id4',
                                                '000004.png',
                                                '#newdir')
        self.assertTrue(expected)

    def test_save_image_exception(self):
        ''' Test _save_image with exception '''
        expected = list_user_images._save_image('/id4',
                                                '000001.png',
                                                '#except')
        self.assertFalse(expected)

    def test_list_user_images(self):
        ''' Test list_user_images '''
        cwd = os.getcwd()
        expected = [('test_id1', cwd + '/test_id1/test_dir1', '000005.png')]
        #path = os.path.join(cwd, 'test_id1')
        self.assertEqual(list_user_images.list_user_image('test_id1'), expected)

    def test_reconcile_images(self):
        ''' Test reconcile_user_images '''
        rec = list_user_images.reconcile_images('test_id1', self.image_collection)
        self.assertEqual(rec[0], rec[1])

    def test_reconcile_images_only_disc(self):
        ''' Test reconcile_user_images only disc storage '''
        rec = list_user_images.reconcile_images('test_id2', self.image_collection)
        self.assertEqual(rec[0], {'000006.png'})

    def test_reconcile_images_only_db(self):
        ''' Test reconcile_user_images only db storage '''
        rec = list_user_images.reconcile_images('id4', self.image_collection)
        self.assertEqual(rec[1], {'000004.png'})

    def test_reconcile_images_no_dir(self):
        ''' Test reconcile_user_images no images stores '''
        rec = list_user_images.reconcile_images('idx', self.image_collection)
        expected = [None, None]
        self.assertEqual(rec, expected)
