# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import crypt, os

# Inspiration -> https://www.vitoshacademy.com/hashing-passwords-in-python/

def hash_pass( password ):
    """Hash a password for storing."""
    password = crypt.crypt(password,crypt.METHOD_MD5)
    return ( password.encode('utf-8') )
