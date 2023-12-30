# AgileBoard 🚀

AgileBoard is a Kanban-style project management tool designed to help teams stay organized & track tasks. 📋✅

## Features 🎯

- Drag and drop tasks to move them between different stages of progress.
- Create, edit, and delete tasks with ease.
- Intuitive user interface for a smooth and seamless experience.
- Dark mode for better visibility during late-night work sessions. 🌙

## Local Setup ⚙️

Follow these simple steps to set up AgileBoard on your local machine:

1. **Clone the repository:**
   ```
   git clone https://github.com/your-username/agileboard.git
   ```

2. **Install docker and docker-compose:**
   ```
   sudo apt-get update
   sudo apt install docker.io && docker-compose
   ```
   You can also visit [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/) to Install the docker engine or install the docker desktop incase you experience any issue with the command above

3. **Run docker-compose to install the dependencies and build the application:**
   ```
   cd agileboard
   docker-compose up -d --build
   docker-compose exec backend python manage.py migrate
   ```

6. **Open the app in your browser:**
   Visit [http://localhost:3000](http://localhost:3000) to see AgileBoard in action!


## License 📝

AgileBoard is licensed under the [MIT License](https://opensource.org/licenses/MIT).

Thank you for checking out AgileBoard! We hope you find it useful for managing your projects. If you have any questions or need assistance, please don't hesitate to reach out.

Happy task management! 🎉
