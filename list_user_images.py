#!/usr/bin/env python3
# 06/25/2021
# Dev: Cody Yarger
# Assignment 09 - Advanced Language Constructs

'''
    User image functions for social network project
'''
# pylint: disable=C0103
# pylint: disable=R1710
# pylint: disable=W1203

import os
import peewee as pw
from log_image_operations import log, logger


@log
def add_image(user_id, tags, user_collection, image_collection):
    '''
        Adds a user image to the database and saves image to disc
    '''

    # check tag length and format
    if len(tags) > 100:
        logger.info('Error: tag > 100 characters')
        return False

    check_tag = tags.split(' ')
    for tag in check_tag:
        try:
            if tag.replace(' ', '')[0] != '#':
                return False
        except IndexError:
            continue

    # process picture_id filename and call load_image and save_image
    if user_collection.find_one(user_id=user_id):
        if image_collection.find_one(picture_id='000001.png'):   # store picture_ids to list
            picid_record = []
            for row in image_collection:
                picid_record.append(row['picture_id'])

            # convert picture_id to int, add 1, convert back to picture_id string
            picid = int((picid_record[-1].lstrip('0')).split('.', 1)[0]) + 1
            picture_id = str(picid).zfill(6) + '.png'
        else:
            picture_id = ("1".zfill(6) + '.png')

        if _load_image(user_id, picture_id, tags, image_collection) &\
                _save_image(user_id, picture_id, tags):
            return True
    else:
        logger.info(f'No user_id {user_id} in the database')
        return False


@log
def _load_image(user_id, picture_id, tags, image_collection):
    '''
        Helper function to load image file names to db
    '''
    try:
        image_collection.insert(user_id=user_id,
                                picture_id=picture_id,
                                tags=tags)

        logger.info(f'picture_id {picture_id} added to database')
        return True
    except pw.IntegrityError:
        logger.info(f'Error adding picture id: {picture_id} to database')
        return False


@log
def _save_image(user_id, picture_id, tags):
    '''
        Helper function to save image to disc
    '''
    # define path to image directory
    clean_tag = tags.replace(' ', '')
    cwd = os.getcwd()
    home_path = os.path.join(cwd, user_id)
    full_path = os.path.join(home_path, *clean_tag.split('#'))

    try:
        if os.path.isdir(full_path):
            f = open(full_path + '/' + picture_id, 'wb')
        else:
            os.makedirs(full_path)
            f = open(full_path + '/' + picture_id, 'wb')
        f.write('-'.encode())
        f.close()
        logger.info(f'Image path {full_path} created and file written')
        return True
    except PermissionError:
        return False


@log
def list_user_image(user_id):
    '''
        Returns list of tuples containing user image file structure
    '''
    # get path of user_id image directory
    cwd = os.getcwd()
    path = os.path.join(cwd, user_id)
    if not os.path.isdir(path):
        logger.info('No directory with user_id as name')
        return False
    userid = user_id
    img_list = []

    def list_image_inner(path):

        image_directory = os.path.abspath(path)
        # list of files in home_path
        user_directory_files = os.listdir(image_directory)

        # recursively traverse all directories and files
        for filename in user_directory_files:
            filepath = os.path.join(image_directory, filename)
            # if file append user_id, path and file name to list
            if os.path.isfile(filepath):
                img_list.append((userid,
                                 str(filepath.rsplit('/', 1)[0]),
                                 filename))
            # else is directory call list_user_images
            elif os.path.isdir(filepath):
                list_image_inner(filepath)
        logger.info('Image list created')
        return img_list
    return list_image_inner(path)


@log
def reconcile_images(user_id, image_collection):
    '''
        Returns collection of images stored on disc and database
    '''
    # initialize image lists
    disc_images = []
    datab_images = []
    compare_images = []

    # process on-disc images
    on_disc_imgs = list_user_image(user_id)
    if not on_disc_imgs:
        compare_images.append(None)
    else:
        for images in on_disc_imgs:
            disc_images.append(images[2])
        compare_images.append(set(disc_images))

    # process db images
    db_images = image_collection.find(user_id=user_id)
    if db_images:
        for image in db_images:
            datab_images.append(image['picture_id'])
        compare_images.append(set(datab_images))
    else:
        compare_images.append(None)

    if disc_images or db_images:
        return compare_images
    logger.info('No images stored for given user')
    return [None, None]
