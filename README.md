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
   [git clone https://github.com/your-username/agileboard.git](https://github.com/Damisicode/AgileBoard.git)
   ```

2. **Install docker and docker-compose:**
   ```
   sudo apt-get update
   sudo apt install docker.io && docker-compose
   sudo usermod -aG docker $USER   # Give your user the permission to use docker
   sudo rm -fr /var/run/docker.sock
   sudo reboot   # This will reboot your system to configure the settings
   ```
   You can also visit [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/) to Install the docker engine or install the docker desktop incase you experience any issue with the command above

3. **Generate a secret key from [djecrety.ir](djecrety)**

4. **Set environmental variables:**
   ```
   SECRET_KEY=<YOUR SECRET KEY>
   POSTGRES_DB=<YOUR POSTGRESQL DATABASE PORT>
   POSTGRES_PASSWORD=<YOUR POSTGRESQL PASSWORD>
   ENVIRONMENT='development'
   ```

3. **Run docker-compose to install the dependencies and build the application:**
   ```
   cd agileboard
   docker-compose up -d --build
   docker-compose exec backend python backend/manage.py migrate
   ```

4. **Create Super User to access the API:**
   ```
   docker-compose exec backend python backend/manage.py createsuperuser
   ```

6. **Open the API in your browser:**
   Visit [http://localhost:8000/swagger-docs](http://localhost:8000/swagger-docs) to access the AgileBoard API in action!


## License 📝

AgileBoard is licensed under the [MIT License](https://opensource.org/licenses/MIT).

Thank you for checking out AgileBoard! We hope you find it useful for managing your projects. If you have any questions or need assistance, please don't hesitate to reach out.

Happy task management! 🎉
