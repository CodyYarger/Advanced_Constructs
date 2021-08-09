#!/usr/bin/env python3
# 06/25/2021
# Dev: Cody Yarger
# Assignment 09 - Advanced Language Constructs
'''
    User functions for social network project
'''
# pylint: disable=E1101
# pylint: disable=R0201

from loguru import logger
import peewee as pw


# @pysnooper.snoop()
def add_user(user_id, user_name, user_last_name, email, user_collection):
    '''
        Adds a new user to user collection
    '''
    if len(user_id) > 30 or len(user_name) > 30 or len(user_last_name) > 100:
        logger.info('user_id/name > 30, or user_last_name > 100, characters')
        return False

    try:
        user_collection.insert(user_id=user_id,
                               user_name=user_name,
                               user_last_name=user_last_name,
                               email=email)

        logger.info(f'user_id {user_id} added to database')
        return True
    except pw.IntegrityError:
        logger.info(f'user_id {user_id} in database of len user_id > 30')
        return False


# @pysnooper.snoop()
def modify_user(user_id, user_name, user_last_name, email, user_collection):
    '''
        Modifies an existing Model Instance
    '''
    if len(user_id) > 30 or len(user_name) > 30 or len(user_last_name) > 100:
        logger.info('user_id/name > 30, or user_last_name > 100, characters')
        return False

    if user_collection.find_one(user_id=user_id):
        user_collection.update(user_id=user_id,
                               user_name=user_name,
                               user_last_name=user_last_name,
                               email=email,
                               columns=['user_id']
                               )
        logger.info(f'user_id {user_id} modified')
        return True
    logger.info(f'No user_id {user_id} in the database')
    return False


# @pysnooper.snoop()
def delete_user(user_id, user_collection, status_collection):
    '''
        Deletes user from user_collection
    '''
    if user_collection.find_one(user_id=user_id):
        user_collection.delete(user_id=user_id)
        status_collection.delete(user_id=user_id)
        logger.info(f'user_id {user_id} and status deleted')
        return True
    logger.info(f'No user_id {user_id} in the database')
    return False


# @pysnooper.snoop()
def search_user(user_id, user_collection):
    '''
        Searches for existing user in user_collection
    '''
    query = user_collection.find_one(user_id=user_id)
    if query:
        logger.info(f'user_id {user_id} found')
        return query
    logger.info(f'No user_id {user_id} in the database')
    return False
