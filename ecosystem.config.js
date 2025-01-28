module.exports = {
  apps: [
    {
      name: "MuscleFuel", // Name of your app
      script: "gunicorn", // Gunicorn as the script to run
      args: "MuscleFuel.wsgi:application --workers 2", // Gunicorn args (entry point and number of workers)
      env: {
        DJANGO_SETTINGS_MODULE: "MuscleFuel.settings", // Django settings module
        PYTHONPATH: "/home/ec2-user/MuscleFuel/venv/lib/python3.x/site-packages", // Path to the site packages of your virtual environment
      },
      cwd: "/home/ec2-user/MuscleFuel", // Path to your project directory
      max_memory_restart: "1G", // Auto restart if app exceeds 1GB memory usage
      interpreter: "/home/ec2-user/MuscleFuel/venv/bin/python", // Specify Python interpreter in the virtual environment
    },
  ],
};
