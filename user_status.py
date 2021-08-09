#!/usr/bin/env python3
# 06/25/2021
# Dev: Cody Yarger
# Assignment 08 - Relational Database - DataSet API
'''
    User status functions for social network project
'''

from loguru import logger
import peewee as pw
# pylint: disable=E1101
# pylint: disable=R0201


def add_status(user_id,
               status_id,
               status_text,
               status_collection,
               user_collection):
    '''
        Adds new status to user status collection
    '''
    try:
        user_collection.insert(user_id=user_id)
        logger.info(f'user_id {user_id} not in database')
        user_collection.delete(user_id=user_id)
    except pw.IntegrityError:
        logger.info(f'user_id {user_id} in database status added')
        status_collection.insert(user_id=user_id,
                                 status_id=status_id,
                                 status_text=status_text)
        logger.info(f'user_id {user_id} status added to database')
        return True
    logger.info(f'status_id {status_id} already in database')
    return False


def modify_status(status_id,
                  status_text,
                  status_collection):
    '''
        Modifies user status
    '''
    query = status_collection.find_one(status_id=status_id)
    if query:
        status_collection.update(status_id=status_id,
                                 status_text=status_text,
                                 columns=["status_id"]
                                 )
        logger.info(f'status_id {status_id} status text modified')
        return True
    logger.info(f'No status_id {status_id} in the database')
    return False


def delete_status(status_id, status_collection):
    '''
        Deletes user status from status_collection
    '''
    if status_collection.find_one(status_id=status_id):
        status_collection.delete(status_id=status_id)
        logger.info(f'status_id {status_id} deleted')
        return True
    logger.info(f'No status_id {status_id} in the database')
    return False


def search_status(status_id, status_collection):
    '''
        Searches for existing status in status_collection
    '''
    query = status_collection.find_one(status_id=status_id)
    if query:
        logger.info(f'status_id {status_id} found')
        return query
    logger.info(f'No status_id {status_id} in the database')
    return False
