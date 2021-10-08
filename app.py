#!/usr/bin/env python
# coding: utf-8

# In[5]:


import os
import streamlit as st
import numpy as np
from PIL import  Image
import time
#passlib,hashlib,bcrypt,scrypt
import hashlib
from multipage import MultiPage
import sqlite3 

#import translator, About, Record

# Create an instance of the app 
#app = MultiPage()
image = Image.open('Logo.png')
st.image(image, use_column_width=True)

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns([3,2,1])

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
conn = sqlite3.connect('data.db')
c = conn.cursor()
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')
def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()
def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def main():
	username = st.text_input("User Name")
	password = st.text_input("Password",type='password')
	if st.button("Login"):
		create_usertable()
		hashed_pswd = make_hashes(password)
		result = login_user(username,check_hashes(password,hashed_pswd))
		if result:
		      st.success("Logged In as {}".format(username))
		      task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
		else:
		   st.warning("Incorrect Username/Password")


	if st.button("Register"):
	     #st.subheader("Create New Account")
	     #new_user = st.text_input("Enter Username")
	     #new_password = st.text_input("Enter Password",type='password')
             #time.sleep(5) 
             create_usertable()
             add_userdata(username,make_hashes(password))
             st.success("You have successfully created a valid Account")
             st.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()