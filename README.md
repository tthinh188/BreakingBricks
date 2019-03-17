# Breakout

## Purpose
Labs 10-14 will constitute the remainder of the semester and will involve the development of the classic Atari game Breakout.
Lab 9 was an introduction to working in real-time environments.
Now that you have had time to play with and experiments with developed code, it is time to start writing it yourself.

That being said, these labs serve 3 main purposes:
* Giving you exposure to larger codebases (similar to the first incremental project).
* Working with and achieving __milestones__ (you may already be familiar with this if you've taken ENGR 121).
* Working as part of a team to achieve success in coding.
 
> __PAIRED PROGRAMMING:__ We will be implementing paired programming in a similar fashion as the previous half of the semester.
Working as part of a group always presents a new set of challenges due to the differences and opinions of others.
I encourage everyone to treat this project as an opportunity to improve collaborating with others (even if you are already an excellent programmer).
Always keep in mind that companies are looking for individuals who can work well with a team, this is true across every discipline.

>__TAKE AWAY:__ At the end of the semester, you should have something that you would be proud to show off to your friends and family.
You may also be able to add this project as part of your resume when you're looking for internships.

## Schedule
In order to better help you succeed at this project, we have divided it into 5 parts.
Each part will consist of a 1-Week lab, and will have milestones that you will be required to meet.
The last lab of the semester will not be a work lab, but instead a time to present what you've achieved.

> __NOTE:__ This schedule and milestones of _future labs_ are subject to changes depending on the status of most groups.

* __Lab 10 - Inheritance__
  * This lab will focus on implementing game objects as the children of PyGame Sprites.
  * This lab will have you create all objects and multiple, different bricks.
* __Lab 11 - Real-time programming II__
  * This lab will focus on working in the update loop.
  * Unlike lab 9, there will be a larger emphasis on debugging movement code and fixing issues related to real-time systems.
  * In this lab you should also begin to track items such as lives and levels.
* __Lab 12 - Binary File I/O__
  * This lab will focus on using File I/O to store gamedata and allow a game to be saved.
* __Lab 13 - Integration__
  * This lab is designed to give you a week to add your own touches to the game.
  * Ideas will be given, but feel free to add whatever you want to the game.
  * This lab will offer you an opportunity to catch up if you have fallen behind.
* __Lab 14 - Presentations__
  * This week will consist of the end-of-semester "Super" quiz.
  * You will present your projects in 5 minute time slots.

>__NOTE: EVEN THOUGH THE ENTIRETY OF THE PROJECT WILL BE GIVEN IN WEEK 10, WE STRONGLY DISCOURAGE TEAMS FROM GOING AHEAD.
IF YOU AND YOUR PARTNER CHOOSE TO WORK AHEAD, PLEASE WORK TOGETHER, ANY CODE WHICH WAS NOT WORKED ON JOINTLY WILL NOT RECEIVE PARTICIPATION CREDIT.__

### Grading Overview
* 100 points | Week 10 Milestones (graded on Week 11)
* 100 points | Week 11 Milestones (graded on Week 12)
* 100 points | Week 12 Milestones (graded on Week 13)
* 100 points | Week 13 Milestones (graded on Week 14)
* 100 points | Week 14 Presentation
* 300 points | Final Project Submission (due during finals week [date TBD])

All weeks will count the same as a normal lab (100 points).
The final presentation will also count as a normal lab grade.
The final project submission will be due during finals week and will give you an opportunity to reclaim points if you've missed some milestones.

# Lab 10 - Inheritance
This lab will be based on utilizing inheritance to help facilitate creating game objects.

__Why should we use inheritance?__
If you remember from lecture, child objects inherit attributes and functions from their parents.
In the case of PyGame and game development in general, a lot of work is required to setup a valid game object.
Fortunately, PyGame comes equipped with the `Sprite` class in the `sprite` module (`pygame.sprite.Sprite`).
This sprite object is a template that is already setup to work seamlessly in PyGame.

## Understanding Sprites

All sprites are composed of 2 primary elements, an image (which is what is seen on screen), and a collision field (which is used to determine the bounds of an object).
By separating these 2 elements, you gain increased control over the physics in the game environment.

The important object to take note of in this relationship is the bounding box, which is a nested class called `pygame.Rect`.
When you instantiate a new sprite object, you can refer to its bounding box via the `rect` attribute (e.g. `mysprite.rect`).
This bounding box is the principle method behind moving objects on screen (think about when you moved the paddle to the bottom of the screen in Lab 9).
There are 2 ways of easily moving sprites, the first is to use the `move` function, and the second is to use the sub-points on the rectangle (more on that later).
The move function is essentially a setter for the sprite, it takes in a list containing an x and y coordinate and moves the ball to the location specified.
The location is based on the screen location where the top left corner is the origin and the x-axis increased to the right, and the y-axis increases when going down (Y is inverted from a normal Cartesian coordinate system).

The other method, as described above, is to use the subpoints of the Rect object.
These points refer to 9 points on the rectangle's perimeter: `topleft`, `bottomleft`, `topright`, `bottomright`, `midtop`, `midleft`, `midbottom`, `midright`, and `center`. 
All of these points are set with a tuple containing an x and a y position (e.g. `(x, y)`).
There are also other dimensions which may be used to align the sprite, these include:
* `x` and `y`, which refers to the top left of the sprite.
* `top`, `left`, `bottom`, and `right`, which refers to either the x or y of a given side.
* `centerx` and `centery`, which refer to the x or y of the center of the Sprite.
> __NOTE:__ These dimensions only require single dimensional data, like an int.

As state earlier, you can also influence the size of the object, via its collision box.
This can be done by working with the following variables:
* `size`, which takes in a tuple containing the new width and height
* `width`, and `height`, which contains the elements individually

I recommend looking through the full __[Documentation](https://www.pygame.org/docs/ref/rect.html)__ for a the `pygame.Rect` object, as there is a lot to explore with this object.

## Creating the Objects

For this lab, we need to focus on 3 objects: a ball, a paddle, and a brick.
You can use the code from last week as a starting point, however, going forward we will be using this repository.
You should run the game to test your code and make sure that it is working.

### The Ball
The ball will bounce around on the sides of the screen, and will be deflected when it hits a Brick.
It will also be deflected when it hits the paddle.
Unlike in Tom's Pong, however, the ball will not bounce off of the bottom of the screen, but will fall through the screen.
The ball should start on top of the paddle, aligned on to the `centerx` of the screen.
> __NOTE:__ The ball does not need to start out stationary on the paddle or have user input to start, for this lab, having the ball launch from the start is sufficient.

### The Paddle
The paddle will move across the bottom of the screen to deflect the ball upwards.
The paddle should start in the bottom, middle of the screen.
The paddle should not be able to leave the screen.
That is, `screen.left <= paddle.left` and `paddle.right <= screen.right`.

The paddle should deflect the ball based on where the ball lands on the paddle (See below).
![Ball Deflection](/docs/img/ball_deflection.png)

### The Brick
A brick should sit in its designated location and not move.
A brick should have a health value associated with it.
When a ball impacts the brick, it should be damaged.
When a brick's health reaches 0, it should be destroyed (i.e. removed from the screen).

## Submission
For this lab, you will present your results to your instructor in the Week 11 Scrum.
Your instructor will ask additional questions regarding your implementation and other general knowledge.

## Rubric
* 40 - Participation
* 30 - Ball working correctly
  * 5 - Ball starts out on top of the paddle and is bounced upward.
  * 5 - Ball is deflected when it hits the paddle (Movement does not need to be perfect).
  * 20 - Ball is deflected when it hits a brick (Movement does not need to be perfect).
* 20 - Paddle Working correctly
  * 5 - Paddle does not leave the bounds of the screen.
  * 15 - Paddle deflects the ball with an angle based on where the ball hits.
* 30 - Brick working correctly
  * 15 - Bricks should have health that is decreased when a ball hits it.
  * 15 - Bricks should be destroyed when their health reaches 0.

# Lab 11 - Real-Time Programming II
   
## Submission

## Rubric

# Lab 12 - Binary File I/O
   
## Submission

## Rubric

# Lab 13 - Integrations
   
## Submission

## Rubric

# Lab 13 - Presentations

The first 30 minutes of this lab will involve taking the "Super" quiz. Which will count for 2 quiz grades (4% of your overall grade).

The remaining 75 minutes will be spent on group presentations.
Each group will present their project.
I want to see the following information from each group:
* Demo of the game (include multiple levels and power-ups if applicable).
* What challenges did you face during development (from each partner)?
  How did your team solve these?
  > __NOTE:__ These can be both in terms of code and disagreements with the team
* What did you enjoy about the project (from each partner)?
* What did you learn from the project (from each partner)?

You and your partner must present for no fewer than __4 minutes__ and no longer than __6 minutes__.
If your presentation is too long or short I will take off 10 points per minute (__yes, I will be timing__).
> You and your partner should practice presenting before the final lab (At least run through it once)!

If you take longer than 7 minutes, I will likely cut you off (don't make me do this)!

## Submission
In order to receive a grade for this lab, you must be present in lab to present your Breakout game.
I will evaluate your presentation in class.
You are encouraged to submit any supplemental notes or presentations (e.g. A powerpoint), though these are not required.

## Rubric
* 25 - Live demo of your game.
* 40 - Discussion about your project (e.g. Challenges, enjoyment, knowledge gained).
* 35 - Quality of the presentation.
  * Did you keep on topic?
  * Did you speak clearly, concisely, and avoid filler (e.g. "Um", "Like")?
  * Did you have supplemental content (e.g. slides)? (Not necessary, but could help if used correctly).
    * Keep in mind __PowerPoint != Presentation__, don't make slides unless they improve your presentation.

__Presentation Length?__
I will take the final score from above and take off points for going under 4 minutes or over 6 minutes.
For example, a presentation that goes for 6:30 minutes or 3:30 minutes would lose 5 points, while a project that goes for 4:00 minutes exactly or 5:59 minutes would not lose any points.

# Additional Documentation

[Command Line Interfaces](docs/cli.md)

[Installing with pip](docs/numpy_matplotlib_installation.md)

[Instantiation Example](docs/car_example.md)

[PyGame Docs & API](https://www.pygame.org/docs/)
