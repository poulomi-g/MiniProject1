# MiniProject1
  
  Made By: Poulomi Ganguly and Rahul Korde
  
  A CLI for accessing a reddit-like database allowing users to do the following:
  
  After a successful login, users should be able to perform all of the following tasks.

    Post a question.The user should be able to post a question by providing title and body texts. The post should be properly recorded in the database tables. A unique pid should be assigned by your system, the post date should be set to the current date and the poster should be set to the user posting it.
    Search for posts.The user should be able to provide one or more keywords, and the system should retrieve all posts that contain at least one keyword either in title, body, or tag fields. For each matching post, in addition to the columns of posts table, the number of votes, and the number of answers if the post is a question (or zero if the question has no answers) should be displayed. The result should be ordered based on the number of matching keywords with posts matching the largest number of keywords listed on top. If there are more than 5 matching posts, at most 5 matches will be shown at a time, letting the user select a post or see more matches. The user should be able to select a post and perform a post action (as discussed next).
    Post action-Answer. If the selected post is a question, the user should be able to post an answer for the question by providing title and body texts. The answer should be properly recorded in the database tables. A unique pid should be assigned by your system, the post date should be set to the current date and the poster should be set to the user posting it. The answer should be also linked to the question.
    Post action-Vote.The user should be able to vote on the post (if not voted already on the same post). The vote should be recorded in the database with a vno assigned by your system, the vote date set to the current date and the user id is set to the current user.

Privileged users can perform the following post actions in addition to those that can be performed by ordinary users (as discussed above). These actions are not available to ordinary users.

    Post action-Mark as the accepted. The user should be able to mark the post (if it is an answer) as the accepted answer. If the question has already an accepted answer, the user should be prompted if s/he wants to change the accepted answer. The user can select to change the accepted answer or leave it unchanged.
    Post action-Give a badge. The user can give a badge to the poster by providing a badge name. The information is recorded in the database with the badge date set to the current system date.
    Post action-Add a tag. The user should be able to add tags to the post.
    Post Action-Edit. The user should be able to edit the title and/or the body of the post. Other fields are not updated when a post is edited.
