#!/usr/bin/env python3
# 06/25/2021
# Dev: Cody Yarger
# Assignment 09 - Advanced Language Constructs

''' Main for calling social network database modules '''
# pylint: disable=C0103
# pylint: disable=R0903

import os
import csv
from loguru import logger
import peewee as pw
import user_status
import users
import list_user_images


def load_users(filename, user_collection):
    '''
        Opens a CSV file with user data and loads it to a SQL database.
    '''
    cwd = os.getcwd()
    try:
        filename = cwd + "/" + filename + ".csv"
        with open(filename, newline='') as accounts_csv:
            # check for empty cells
            reader = csv.DictReader(accounts_csv)
            for row in reader:
                for _, dvalue in row.items():
                    if dvalue == '':
                        logger.info("Error in CSV file")
                        return False

                # insert user data into db model
                try:
                    user_collection.insert(user_id=row['USER_ID'],
                                           user_name=row['NAME'],
                                           user_last_name=row['LASTNAME'],
                                           email=row['EMAIL'])
                except pw.IntegrityError:
                    return False
            return True
    except (FileNotFoundError, IOError):
        print('Error: File not found')
        return False


def load_status_closure(status_collection, user_collection):
    '''
        Closure for tracking and maintaining state of validated users in the
        user_collection model for loading user status data into user_collection.
    '''
    verified_users = []

    def inner_function(reader):
        for row in reader:

            # check for empty cells in CSV file
            for _, dvalue in row.items():
                if dvalue == '':
                    logger.info("Error in CSV file")
                    return False

            user_id = row['USER_ID']
            valid_user = False

            # if user_id in verified_users list.
            if user_id in verified_users:
                valid_user = True

            # else query user_collection model to see if id exists
            else:
                query = user_collection.find_one(user_id=user_id)
                if query:
                    # add ID to verified_users
                    verified_users.append(user_id)
                    valid_user = True

            # if user id is valid user add to status_collection model
            if valid_user:
                try:
                    status_collection.insert(
                        user_id=row['USER_ID'],
                        status_id=row['STATUS_ID'],
                        status_text=row['STATUS_TEXT'])
                except pw.IntegrityError:
                    return False
            # else user ID not in user_collection dont add to status_collection
            else:
                return False
        # print(verified_users)
        return True
    return inner_function


def load_status_updates(filename, status_collection, user_collection):
    '''
        Opens a CSV file with user data and loads it to a SQL database.
    '''
    cwd = os.getcwd()
    try:
        with open((cwd + "/" + filename + ".csv"), newline='') as status_csv:
            reader = csv.DictReader(status_csv)

            # create instance of closure
            add_records = load_status_closure(status_collection, user_collection)

            # returns True or False from closure inner function
            return add_records(reader)
    except (FileNotFoundError, IOError):
        print('Error: File not found')
        return False
    return True


def load_image_closure(image_collection, user_collection):
    '''
        Closure for tracking and maintaining state of validated users in the
        user_collection model for loading user status data into user_collection.
    '''
    verified_users = []

    def inner_function(reader):
        for row in reader:

            # check for empty cells in CSV file
            for _, dvalue in row.items():
                if dvalue == '':
                    logger.info("Error in CSV file")
                    return False

            user_id = row['USER_ID']
            valid_user = False

            # if user_id in verified_users list.
            if user_id in verified_users:
                valid_user = True

            # else query user_collection model to see if id exists
            else:
                query = user_collection.find_one(user_id=user_id)
                if query:
                    # add ID to verified_users
                    verified_users.append(user_id)
                    valid_user = True

            # if user id is valid user add to image_collection model
            if valid_user:
                try:
                    image_collection.insert(
                        user_id=row['USER_ID'],
                        picture_id=row['PICTURE_ID'],
                        tags=row['TAGS'])
                except pw.IntegrityError:
                    return False
            # else user ID not in user_collection dont add to status_collection
            else:
                return False
        # print(verified_users)
        return True
    return inner_function


def load_user_images(filename, image_collection, user_collection):
    '''
        Opens a CSV file with user image data and loads it to a SQL database
    '''
    cwd = os.getcwd()
    try:
        with open((cwd + "/" + filename + ".csv"), newline='') as image_csv:
            reader = csv.DictReader(image_csv)

            # create instance of closure
            add_records = load_image_closure(image_collection, user_collection)

            # returns True or False from closure inner function
            return add_records(reader)
    except (FileNotFoundError, IOError):
        print('Error: File not found')
        return False
    return True


def add_user(user_id, user_name, user_last_name, email,  user_collection):
    '''
        Adds new user to the database
    '''
    return users.add_user(user_id, user_name, user_last_name, email,  user_collection)


def update_user(user_id, user_name, user_last_name, email,  user_collection):
    '''
        Updates the values of an existing user
    '''
    return users.modify_user(user_id,
                             user_name,
                             user_last_name,
                             email,
                             user_collection)


def delete_user(user_id, user_collection, status_collection):
    '''
        Deletes a user from user_collection
    '''
    return users.delete_user(user_id, user_collection, status_collection)


def search_user(user_id, user_collection):
    '''
        Searches for a user in user_collection
    '''
    return users.search_user(user_id, user_collection)


def add_status(user_id,
               status_id,
               status_text,
               status_collection,
               user_collection):
    '''
        Adds a user status to status_collection
    '''
    return user_status.add_status(user_id,
                                  status_id,
                                  status_text,
                                  status_collection,
                                  user_collection)


def update_status(status_id,
                  status_text,
                  status_collection):
    '''
        Updates the values of an existing status_id
    '''
    return user_status.modify_status(status_id,
                                     status_text,
                                     status_collection)


def delete_status(status_id, status_collection):
    '''
        Deletes a status_id from status_collection
    '''
    return user_status.delete_status(status_id, status_collection)


def search_status(status_id, status_collection):
    '''
        Searches for a status in status_collection
    '''
    return user_status.search_status(status_id, status_collection)


def add_image(user_id, tag, user_collection, image_collection):
    '''
        Adds user image to tag directory structure
    '''
    return list_user_images.add_image(user_id, tag, user_collection, image_collection)


def list_user_image(user_id):
    '''
        Lists a users images stored on disc
    '''
    return list_user_images.list_user_image(user_id)


def reconcile_images(user_id, image_collection):
    '''
        Adds user image to tag directory structure
    '''
    return list_user_images.reconcile_images(user_id, image_collection)
