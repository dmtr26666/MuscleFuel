# Documentation

### Project Overview

MuscleFuel is a dynamic platform designed for food enthusiasts who want to explore, organize, and share their favorite protein recipes.
It provides a personalized space where users can gather and store all their cherished recipes in one convenient place, whether they come from personal creations, shared collections, or discoveries within the MuscleFuel community.

---

### Setup Tutorials

1. Clone the repository:
   ```sh
   git clone https://github.com/dmtr26666/MuscleFuel.git
   ```
2. Create a virtual environment:
   ```sh
    python -m venv .venv
    ```
3. Install requirements.txt:
   ```sh
   pip install -r requirements.txt
   ```
4. Configure .env file
5. Setup postgres docker container
6. Run migrations:
   ```sh
   python manage.py migrate
   ```
7. Add initial db objects:
   ```sh
    python manage.py loaddata MuscleFuel/recipes/fixtures/recipes.json
   ```
8. Run the project


---

### Key features

- Recipe Collection: Save and manage your favorite recipes from various sources and organize them within your profile.
- Explore and Discover: Browse through a diverse selection of high-protein recipes shared by other users, from quick, protein-packed snacks to hearty, muscle-fueling meals.
- Share with the Community: Publish your own recipes for others to discover and enjoy. Share your cooking skills, tips, and creativity with a like-minded audience.
- Favorites and Organization: Easily mark recipes as favorites to revisit them later and organize them for quick access.
- Moderation and Quality Control: Recipes can be reviewed and approved by moderators to maintain high-quality content and a positive user experience.

---
