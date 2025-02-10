# Cocktails_app_V2
### **Cocktail App: Project Summary & Flow**

#### **Overview**
This project is a **cocktail recipe management application** with a **GUI built using PyQt**. It uses **SQLite** as the primary database and **dictionaries (caching) for real-time lookups** to improve performance. The app helps users manage their liquor inventory and suggests cocktails based on available ingredients.

---

### **Main Components & Workflow**

#### **1. Database Handling**
- The SQLite database (`cocktails.db`) contains a **cocktails table** storing detailed cocktail recipes.
- The table includes:
  - `id` (Primary Key)
  - `name`
  - `abv` (Alcohol by Volume)
  - `is_easy_to_make`
  - `ingredients` (stored as a JSON string)
  - `instructions`
  - `personal_notes`
  - `is_favorite`
  - `times_made`
  - `prep_method`
  - `made_from` (main ingredients)
  - `flavor` (categorized as **Sour & Tart, Fruity & Tropical, etc.**)
  - `glass_type`
  - `garnish`

#### **2. Data Import Process**
- Cocktail recipes are stored in a **JSON file** (`cocktail_book.json`).
- A script **parses the JSON** and inserts the data into SQLite.
- The data is cleaned and formatted properly before insertion (e.g., `ingredients` stored as JSON strings).

#### **3. Database Caching with `cocktail_db.py`**
- **Purpose**: To reduce direct database queries and improve performance.
- **Implementation**:
  - Data is loaded **from SQLite into a dictionary (`cache`)** when the app starts.
  - The `load_cache()` method queries all cocktails and stores them in-memory.
  - The `add_cocktail()` method updates both the **database** and **cache** in real-time.

#### **4. GUI Interaction (PyQt)**
- The **GUI allows users to search for, filter, and favorite cocktails**.
- Users can:
  - Browse the cocktail list.
  - Search by name, ingredients, or flavor.
  - View cocktail details, including preparation method, glass type, and garnish.
  - Mark cocktails as favorites or track how many times they’ve been made.

#### **5. Ingredient-Based Suggestions**
- The **app suggests cocktails based on available ingredients** in the user’s inventory.
- **Matching Algorithm**:
  - The app checks whether all ingredients in a cocktail recipe exist in the inventory.
  - If **all required ingredients** are available, the cocktail is suggested.
  - If **some ingredients** are missing, the app can suggest substitutions.

#### **6. Real-Time Performance Optimization**
- **Dictionaries (`cache`) are used for quick lookups** instead of querying SQLite for every request.
- The **GUI retrieves cocktail data from memory**, reducing database calls.
- When a cocktail is **added/edited**, the **cache is updated simultaneously**.

---

### **Summary of the System Flow**
1. **Data Import**: JSON → SQLite (`cocktails.db`)
2. **Data Caching**: SQLite → Python Dictionary (`cache`)
3. **GUI Interaction**:
   - Display & search for cocktails
   - Suggest drinks based on available ingredients
   - Allow users to mark favorites
4. **Database Updates**:
   - Add new cocktails
   - Modify records (favorite status, times made)
   - Update cache in real-time

---

### **Why This Design?**
- **Performance**: Cache reduces SQL queries.
- **Scalability**: The system is structured for easy expansions.
- **User Experience**: The app provides **fast, interactive recommendations**.

Would you like any refinements to this summary? 🚀
