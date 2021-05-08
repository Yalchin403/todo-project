# Todo project

Users can create, update, delete tasks
Each task has a title, description, and deadline
The task can be shared with other users by specifying their usernames. While sharing the task, we can render permission for being able to write comments. If allowed, shared users can write a real-time comment (django-channels is used for this purpose).
There is also celery worker doing background task, which periodically checks database to see if there is any task which is not done yet and deadline is so close (10 minutes before deadline). If there is, email to the owner of the task will be sent to notify the user.

Additionally, there will be multiple databases, one for saving user info, and the other one for handling data coming from apps. Eventually web app will be server by docker compose.