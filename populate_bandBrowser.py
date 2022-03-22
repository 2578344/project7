import os
import datetime
from datetime import timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE','project7.settings')

import django
django.setup()
from BandBrowser.models import UserProfile, Band, Post
from django.contrib.auth.models import User

userProfileInstances =[]#UserProflie instances not User
bandInstances =[]
postInstances =[]
def populate():

    print("===================")

    deleteInstances()#clear any current instances (that are not admin) and replace with the data set

    print("===================")

    usersRaw = [
        {"username":"Alex","instruments":"Banjo","Bio":"Hi","numberOfBands":0,"numberOfPostsActive":0},
        {"username":"John","instruments":"Guitar","Bio":"Hello","numberOfBands":0,"numberOfPostsActive":0},
        {"username":"Tom","instruments":"Drums","Bio":"Howdy","numberOfBands":0,"numberOfPostsActive":0},
        {"username":"Ian","instruments":"Vocals","Bio":"Hello there","numberOfBands":0,"numberOfPostsActive":0},
        {"username":"Peter","instruments":"Bass","Bio":"Hi ya","numberOfBands":0,"numberOfPostsActive":0}
    ]

    bandsRaw = [
        {"name":"Joy Division","genres":"Post Punk","commitment":"Full Time","location":"Manchester","dateCreated":datetime.date(1976, 10, 19)},
        {"name":"The Joy Formidable","genres":"Alternative","commitment":"When We can","location":"Wales","dateCreated":datetime.date(2007, 12, 8)},
        {"name":"Interpol","genres":"Post Punk","commitment":"Weekly","location":"New York","dateCreated":datetime.date(1997, 5, 28)}
    ]

    postsRaw = [
        {"postID":"0","description":"ASAP","title":"Looking For a bassist","publishDate":datetime.date(2022, 3, 9),"expireDate":datetime.date(2022, 3, 9)+ timedelta(days=10),"experienceRequired":"Some","genres":"Post Punk","commitment":"Full Time","location":"Manchester","Type":"Band"},
        {"postID":"1","description":"Just Started the band","title":"Looking For a drummer","publishDate":datetime.date(2022, 3, 16),"expireDate":datetime.date(2022, 3, 16)+ timedelta(days=10),"experienceRequired":"None","genres":"Alternative","commitment":"When We can","location":"Wales","Type":"Band"},
        {"postID":"2","description":"Guitarist seeks band","title":"Looking For Band as a guitarist","publishDate":datetime.date(2022, 3, 22),"expireDate":datetime.date(2022, 3, 22)+ timedelta(days=10),"experienceRequired":"A lot","genres":"Jazz","commitment":"Full Time","location":"Glasgow","Type":"User"}
    ]

    #create User and UserProfile objects, link them together
    for user_data in usersRaw:
        if not User.objects.filter(username=user_data["username"]).exists():
            user = add_User(user_data["username"])
            user.save()
            add_UserProfile(user,user_data["instruments"],user_data["Bio"],user_data["numberOfBands"],user_data["numberOfPostsActive"])

    print("===================")

    #create Band objects
    for band_data in bandsRaw:
        if not Band.objects.filter(name=band_data["name"]).exists():
            add_band(band_data["name"],band_data["genres"],band_data["commitment"],band_data["location"],band_data["dateCreated"])

    print("===================")

    #create Post objects
    for post_data in postsRaw:
        if not Post.objects.filter(postID=post_data["postID"]).exists():
           add_post(post_data["postID"],post_data["description"],post_data["title"],post_data["publishDate"],post_data["expireDate"],post_data["experienceRequired"],post_data["genres"],post_data["commitment"],post_data["location"])

    print("===================")

    #attach posts (manually to user and band models), this adds both links to in both directions
    attachBandToUser(bandInstances[0],userProfileInstances[3])# ian joins Joy Division
    attachBandToUser(bandInstances[2],userProfileInstances[0])# Alex joins Interpol
    attachBandToUser(bandInstances[1],userProfileInstances[2])# Tom joins The Joy formidable

    print("===================")

    #attach posts (manually to user and band models)
    attachPostToUser(postInstances[2], userProfileInstances[1])#john and guitarist seeks band
    attachPostToBand(postInstances[1], bandInstances[1])#The Joy Formidable looking for a drummer
    attachPostToBand(postInstances[0], bandInstances[0])#Joy Division looking for a bassist

    print("===================")
    attachUserToBandAsPotentialMember(userProfileInstances[4],bandInstances[0])# peter requests to join joy division

#user functions
def add_User(username,email=None, password=None):
    user = User.objects.create_user(username, email, password)
    return user

def add_UserProfile(user,instruments,bio,numberOfBands=0,numberOfPostsActive=0):
    userProfile = UserProfile.objects.get_or_create(user=user)[0]
    userProfile.instruments =instruments
    userProfile.linkedAccounts =""
    userProfile.bio = bio
    userProfile.numberOfBands =numberOfBands
    userProfile.numberOfPostsActive =numberOfPostsActive
    userProfile.save()
    print(userProfile.user.username +" Account has been created")
    userProfileInstances.append(userProfile)
    return userProfile

def attachPostToUser(post, userProfile):
    posts = userProfile.post
    if not posts.exists():
        userProfile.post.add(post)
        userProfile.numberOfPostsActive = userProfile.numberOfPostsActive +1
        userProfile.save()
        print(userProfile.user.username+" is "+ post.title+ "!")

def attachBandToUser(bandToJoin, userProfile):
    #first we add the band to the user
    band = userProfile.band.filter(name=bandToJoin.name)
    if not band.exists():
        userProfile.band.add(bandToJoin)
        userProfile.numberOfBands = userProfile.numberOfBands +1
        userProfile.save()
        #now we need to add the user to the band
        attachUserToBandAsCurrentMember(userProfile,bandToJoin)



#band functions
def add_band(name,genres,commitment,location,dateCreated):
    band = Band.objects.get_or_create(name=name)[0]
    band.genres = genres
    band.commitment = commitment
    band.location = location
    band.dateCreated = dateCreated
    band.numberOfPostsActive = 0
    band.numberOfCurrentMembers = 0
    band.numberOfPotentialMembers = 0
    band.save()
    print(band.name +" Band has been created")
    bandInstances.append(band)
    return band

def attachPostToBand(post, band):
    posts = band.post
    if not posts.exists():
        band.post.add(post)
        band.numberOfPostsActive = band.numberOfPostsActive +1
        band.save()
        print(band.name+" "+ post.title+ "!")

def attachUserToBandAsCurrentMember(userProfileToJoin,band):
    user = band.currentMember.filter(username= userProfileToJoin.user.username)
    if not user.exists():
        band.currentMember.add(userProfileToJoin.user)
        band.numberOfCurrentMembers = band.numberOfCurrentMembers +1
        band.save()
        print(userProfileToJoin.user.username+" has joined "+ band.name+ "!")

def attachUserToBandAsPotentialMember(userProfileToRequest,band):
    user = band.potentialMember.filter(username= userProfileToRequest.user.username)
    if not user.exists():
        band.potentialMember.add(userProfileToRequest.user)
        band.numberOfPotentialMembers = band.numberOfPotentialMembers +1
        band.save()
        print(userProfileToRequest.user.username+" has requested to join "+ band.name+ "!")



#post functions
def add_post(postID,description,title,publishDate,expireDate,experienceRequired,genre,commitment,location):
    post = Post.objects.get_or_create(postID=postID)[0]
    post.title = title
    post.publishDate = publishDate
    post.expireDate = expireDate
    post.experienceRequired = experienceRequired
    post.location = location
    post.genre = genre
    post.commitment = commitment
    post.description = description
    post.save()
    print(post.title +" Post has been created")
    postInstances.append(post)
    return post



#all objects functions
def getInstances():
    for band in Band.objects.all():
        if not band in bandInstances:
            bandInstances.append(bandInstances)
        print(band.name+" added")
    for user in UserProfile.objects.all():
        if not user.user in userProfileInstances:
            userProfileInstances.append(user.user)
        print(user.user.username+" added")
    for post in Post.objects.all():
        if not post in postInstances:
            postInstances.append(post)
        print(post.title+" added")

def deleteInstances():
    print("Previous records have been deleted")
    for band in Band.objects.all():
        band.delete()
    for user in User.objects.filter(is_staff=False):
        user.delete()
    for post in Post.objects.all():
        post.delete()

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
