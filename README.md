#Blog.

Blog. is a multi user blog.

## Features of blog 

* Signup
* Login
* Logout
* Create a new post
* Comment on post
* Like posts by other users
* Edit posts published by yourself
* Delete posts published by yourself

## Frameworks used

* Jquery
* MaterializeCSS
* Animate
* WOW

## How to use the blog

Link to the live website - [Blog.](https://myblog-160911.appspot.com/)

### How to signup

- Open the link in browser and click on signup button
- Fill the form, email is optional
- Click the submit button

### How to Login

- Open the link in the browser and click on login button
- Provide username and password
- Click login button

### How to create a new post

- Firstly you must be logged in
- Click on New Post 
- Provide post title and content
- Click on publish button

### How to edit a post

- Click on edit post on post from home page or edit from post page
- Make the edit
- Click on publish button

### How to delete a post

- Click on delete post button on post page

### How to like a post

- Logged in user can like a post by other users
- Click on like button on home or post page

### How to comment on post

- Logged in user can comment on post
- Type comment into comment textarea 
- Click post comment button

## How to install the Blog.

### Prerequisite

- To run this project you will need python 2.7 installed in your system.
- Download and install [Google App Engine SDK](https://cloud.google.com/appengine/docs/standard/python/download)

### Running the blog 

*** Can also be installed on Google cloud using same commands***

Git clone the project:
```sh
$ git clone https://github.com/imathus2/blog.git
```

Preview the blog
** Open preview on http://localhost:8080/ **
```sh
$ dev_appserver.py .
```

Deploy the blog
```sh
$ gcloud app deploy
```