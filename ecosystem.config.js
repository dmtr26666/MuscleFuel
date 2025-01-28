module.exports = {
  apps: [
    {
      name: "musclefuel",  // Name of your app
      script: "gunicorn",  // The command to run
      args: "--workers 2 --bind 0.0.0.0:9000 MuscleFuel.wsgi:application",  // Arguments for Gunicorn
      interpreter: "/home/ec2-user/MuscleFuel/venv/bin/python",  // Path to the python interpreter in your virtualenv
      cwd: "/home/ec2-user/MuscleFuel",  // Working directory where the project is located
      env: {
        DJANGO_SETTINGS_MODULE: "MuscleFuel.settings",  // Specify your settings module
      },
      log_file: "/home/ec2-user/MuscleFuel/logs/gunicorn.log",  // Path to your log file
      out_file: "/home/ec2-user/MuscleFuel/logs/gunicorn-out.log",  // Standard output log file
      error_file: "/home/ec2-user/MuscleFuel/logs/gunicorn-error.log",  // Error log file
      pid_file: "/home/ec2-user/MuscleFuel/gunicorn.pid",  // PID file for Gunicorn
    }
  ]
};
