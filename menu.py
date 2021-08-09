#!/usr/bin/env python3
# 06/25/2021
# Dev: Cody Yarger
# Assignment 09 - Advanced Language Constructs

'''
    Provides a basic frontend
'''

# pylint: disable=C0103
# pylint: disable=W0703

import sys
import os
from contextlib import contextmanager
from datetime import datetime
from playhouse.dataset import DataSet
#import pysnooper
from loguru import logger
import main


log_file = datetime.now().strftime("log_%m_%d_%Y.log")
logger.add(log_file, level="INFO")


# @pysnooper.snoop()
def load_users():
    '''
        Loads user accounts from a file
    '''
    filename = input('Enter filename of user file: ')
    if main.load_users(filename, user_collection):
        logger.info(f"{filename} data loaded successfully")
    else:
        logger.info(f"Error loading {filename}.csv")


# @pysnooper.snoop()
def load_status_updates():
    '''
        Loads status updates from a file
    '''
    filename = input('Enter filename for status file: ')
    if main.load_status_updates(filename, status_collection, user_collection):
        logger.info(f"{filename} data loaded successfully")
    else:
        logger.info(f"Error loading {filename}.csv")


# @pysnooper.snoop()
def load_user_images():
    '''
        Loads images from a file
    '''
    filename = input('Enter filename for image file: ')
    if main.load_user_images(filename, image_collection, user_collection):
        logger.info(f"{filename} data loaded successfully")
    else:
        logger.info(f"Error loading {filename}.csv")


# @pysnooper.snoop()
def add_user():
    '''
        Adds a new user into the database
    '''
    user_id = input('User ID: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    email = input('User email: ')

    if not main.add_user(user_id,
                         user_name,
                         user_last_name,
                         email,
                         user_collection
                         ):
        print("Error occurred while trying to add new user")
    else:
        print("User was successfully added")


# @pysnooper.snoop()
def update_user():
    '''
        Updates information for an existing user
    '''
    user_id = input('User ID: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    email = input('User email: ')

    if user_collection.find_one(user_id=user_id):
        if not main.update_user(user_id,
                                user_name,
                                user_last_name,
                                email,
                                user_collection
                                ):

            print("Error occurred while trying to update user")
        print("User was successfully updated")
    else:
        print("Error occurred while trying to update user")


# @pysnooper.snoop()
def search_user():
    '''
        Searches a user in the database
    '''
    user_id = input('Enter user ID to search: ')
    try:
        search = main.search_user(user_id, user_collection)
        print(f'User id: {search["user_id"]}')
        print(f'User name: {search["user_name"]}')
        print(f'User last name: {search["user_last_name"]}')
        print(f'User email: {search["email"]}')
    except TypeError:
        print("Error: User does not exist")


# @pysnooper.snoop()
def delete_user():
    '''
        Deletes user from the database
    '''
    user_id = input('User ID: ')
    if user_collection.find_one(user_id=user_id):
        if not main.delete_user(user_id, user_collection, status_collection):
            print("Error occurred while trying to delete user")
        else:
            print("User was successfully deleted")
    else:
        print("Error occurred while trying to delete user")


# @pysnooper.snoop()
def add_status():
    '''
        Adds a new status into the database
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')

    if not main.add_status(user_id,
                           status_id,
                           status_text,
                           status_collection,
                           user_collection):
        print("Error occurred while trying to add new status")
    else:
        print("New status was successfully added")


# @pysnooper.snoop()
def update_status():
    '''
        Updates information for an existing status
    '''
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if status_collection.find_one(status_id=status_id):
        if not main.update_status(status_id, status_text, status_collection):
            print("Error occurred while trying to update status")
        else:
            print("Status was successfully updated")
    else:
        print("Error occurred while trying to update status")


# @pysnooper.snoop()
def search_status():
    '''
        Searches a status in the database
    '''
    status_id = input('Enter status ID to search: ')
    try:
        search = main.search_status(status_id, status_collection)
        print(f'User id: {search["user_id"]}')
        print(f'Status ID:: {search["status_id"]}')
        print(f'Status text: {search["status_text"]}')
    except TypeError:
        print("Error: Status ID does not exist")


# @pysnooper.snoop()
def delete_status():
    '''
        Deletes status from the database
    '''
    status_id = input('Status ID: ')
    if status_collection.find_one(status_id=status_id):
        if not main.delete_status(status_id, status_collection):
            print("Error occurred while trying to delete status")
        else:
            print("Status was successfully deleted")
    else:
        print("Error occurred while trying to delete status")


# @pysnooper.snoop()
def add_image():
    '''
        Adds user image to database and saves to disc
    '''
    user_id = input('User ID: ')
    tag = input('Input #tag:')
    if user_collection.find_one(user_id=user_id):
        if not main.add_image(user_id, tag, user_collection, image_collection):
            print("Error occurred while trying to add image")
        else:
            print("Image successfully added")
    else:
        print("Error occurred while trying to add image")


# #@pysnooper.snoop()
def list_user_image():
    '''
        Lists a users images stored on disc
    '''
    user_id = input('User ID: ')
    if user_collection.find_one(user_id=user_id):
        try:
            image_list = main.list_user_image(user_id)
            print('-'*80)
            print(f"Images For User {user_id}")
            print('-'*80)
            for images in image_list:
                print(images)
            print('-'*80)
        except TypeError:
            print(f"No images stored for user {user_id}")
    else:
        print("Error occurred while trying to list images")


# #@pysnooper.snoop()
def reconcile_images():
    '''
        Compares images on disc to database for a given user
    '''
    user_id = input('User ID: ')
    if user_collection.find_one(user_id=user_id):

        try:
            # rec[0] = disk images. rec[1] = db images
            rec = main.reconcile_images(user_id, image_collection)

            if rec[1] is None and isinstance(rec[0], set):
                print(f'Images are stored on disc only for user {user_id}: ')
                _reconcile_printer(rec[0])

            elif rec[0] is None and isinstance(rec[1], set):
                print(f'Images are stored on database only for user {user_id}: ')
                _reconcile_printer(rec[1])

            # if database and disc sets have data print unique picture_ids
            elif isinstance(rec[0], set) and isinstance(rec[1], set):
                disc_images = rec[0] - rec[1]
                db_images = rec[1] - rec[0]
                if len(disc_images) == 0 and len(db_images) == 0:
                    print(f'Database and Disc up to date for user {user_id}: ')
                    _reconcile_printer(rec[0])
                else:
                    print(f'Images stored on disc not in database for user {user_id}: ')
                    _reconcile_printer(disc_images)
                    print(f'Images stored on database not on disc for user {user_id}: ')
                    _reconcile_printer(db_images)
            else:
                print(f'There are no images stored for user {user_id}')

        except AttributeError:
            print("Error occurred while trying to reconcile images")
    else:
        print("Error occurred while trying to reconcile image")


def _reconcile_printer(collection):
    print('-'*80)
    for image in collection:
        print(image)
    print('-'*80)


# #@pysnooper.snoop()
def quit_program():
    '''
        Quits program
    '''
    print("Exiting program")
    sys.exit()


@contextmanager
def dataset_connect(connection_type):
    '''
        Context manager for database connection
    '''
    database = DataSet(connection_type)      # connection object
    try:
        yield database        # yeild connection and execute 'with' inner block

    except Exception as e:      # run if exception in with block
        print(f'Failed: {e}')
        if not connection_type:
            raise e

    finally:  # run after with block is exectued
        print("Database closed")
        db.close()
        cwd = os.getcwd()
        db_path = os.path.join(cwd, 'socialnetwork.db')
        if os.path.isfile(db_path):
            os.remove(db_path)


if __name__ == '__main__':

    # call connection manager for database
    connect_type = 'sqlite:///socialnetwork.db'

    with dataset_connect(connect_type) as db:

        # ===========================================================================
        # instantiate Users tables
        user_collection = db['Users']
        user_collection.insert(user_id='dummy',
                               user_name='dummy',
                               user_last_name='dummy',
                               email='dummy'
                               )
        user_collection.create_index(['user_id'], unique=True)
        user_collection.delete(user_id='dummy',
                               user_name='dummy',
                               user_last_name='dummy',
                               email='dummy')

        # ===========================================================================
        status_collection = db['Status']
        status_collection.insert(status_id='dummy',
                                 user_id='dummy',
                                 status_text='dummy')

        status_collection.create_index(['status_id'], unique=True)
        status_collection.delete(status_id='dummy',
                                 user_id='dummy',
                                 status_text='dummy')
        # ===========================================================================
        image_collection = db['Picture']
        image_collection.insert(picture_id='dummy',
                                user_id='dummy',
                                tags='dummy')

        image_collection.create_index(['picture_id'], unique=True)
        image_collection.delete(picture_id='dummy',
                                user_id='dummy',
                                tags='dummy')
        # ===========================================================================

        # user menu
        menu_options = {
            'A': load_users,
            'B': load_status_updates,
            'C': load_user_images,
            'D': add_user,
            'E': update_user,
            'F': search_user,
            'G': delete_user,
            'H': add_status,
            'I': update_status,
            'J': search_status,
            'K': delete_status,
            'L': add_image,
            'M': list_user_image,
            'N': reconcile_images,
            'Q': quit_program
        }
        while True:
            user_selection = input("""
                                A: Load user database
                                B: Load status database
                                C: Load user images
                                D: Add user
                                E: Update user
                                F: Search user
                                G: Delete user
                                H: Add status
                                I: Update status
                                J: Search status
                                K: Delete status
                                L: Add user image
                                M: List user images
                                N: Reconcile user images
                                Q: Quit

                                Please enter your choice: """)
            if user_selection.upper() in menu_options:
                menu_options[user_selection.upper()]()
            else:
                print("Invalid option")
