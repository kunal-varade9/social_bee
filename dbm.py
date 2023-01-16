import pymysql as p

def connect():
    return p.connect(host='localhost', user='root', password='', port=3307, database='socialbee')

def insert_user(t):
    con = connect()
    cur = con.cursor()
    Q = 'insert into user(name,email,profile_image,password,img_filename) values(%s,%s,%s,%s,%s)'
    cur.execute(Q,t)
    Q = 'select id from user where email = %s'
    cur.execute(Q,t[1])
    u_id = cur.fetchone()
    con.commit()
    con.close()
    return u_id[0]

def display_user(u_id):
    con = connect()
    cur = con.cursor()
    Q = 'select * from user where id = %s'
    cur.execute(Q,str(u_id))
    data = cur.fetchall()
    con.commit()
    con.close()
    return data[0]

def update_user(t):
    if len(t) == 4:
        con = connect()
        cur = con.cursor()
        Q = 'update user set name=%s,email=%s,password=%s where id = %s'
        cur.execute(Q,t)
        con.commit()
        con.close()
    else:
        con = connect()
        cur = con.cursor()
        Q = 'update user set name=%s,email=%s,profile_image=%s,password=%s,img_filename=%s where id = %s'
        cur.execute(Q,t)
        con.commit()
        con.close()

def insert_post(t):
    con = connect()
    cur = con.cursor()
    Q = 'insert into post(post,image,user_id,img_filename) values(%s,%s,%s,%s)'
    cur.execute(Q,t)
    # Q = 'select id from post where user_id = %s'
    # cur.execute(Q,t[2])
    # u_id = cur.fetchone()
    con.commit()
    con.close()
    # return u_id[0]

def display_post(u_id):
    con = connect()
    cur = con.cursor()
    Q = 'select * from post where user_id = %s'
    cur.execute(Q,u_id)
    data = cur.fetchall()
    con.commit()
    con.close()
    return data

def postforupdate(p_id):
    con = connect()
    cur = con.cursor()
    Q = 'select * from post where id = %s'
    cur.execute(Q,p_id)
    data = cur.fetchone()
    con.commit()
    con.close()
    return data


def update_post(t):
    if len(t) == 2:
        con = connect()
        cur = con.cursor()
        Q = 'update post set post=%s where id = %s'
        cur.execute(Q,t)
        con.commit()
        con.close()
    else:
        con = connect()
        cur = con.cursor()
        Q = 'update post set post=%s,image=%s,img_filename=%s where id = %s'
        cur.execute(Q,t)
        con.commit()
        con.close()

def delete_post(p_id):
    con = connect()
    cur = con.cursor()
    Q = 'delete from post where id = %s'
    cur.execute(Q,p_id)
    con.commit()
    con.close()

def check_user(email):
    con = connect()
    cur = con.cursor()
    Q = 'select id,email,password from user where email = %s'
    cur.execute(Q,email)
    cred = cur.fetchone()
    con.commit()
    con.close()
    return cred

def fetchallposts():
    con = connect()
    cur = con.cursor()
    Q = 'select post.* , user.name from post inner join user on post.user_id = user.id;'
    cur.execute(Q)
    posts = cur.fetchall()
    con.commit()
    con.close()
    return posts

def date_add(d):
    con = connect()
    cur = con.cursor()
    Q = 'insert into dummy value (%s)'
    cur.execute(Q,d)
    con.commit()
    con.close()



