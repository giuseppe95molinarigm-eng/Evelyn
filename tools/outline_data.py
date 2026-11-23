"""Content for Milestone 1: title, subtitle, description and 150-recipe outline."""

TITLE = "The Complete Amish Dry Mix Pantry Cookbook"
SUBTITLE = ("150 Budget-Friendly Homemade Dry Mixes and Meals from Scratch, with Baking, "
            "Soup and Seasoning Blends, Mixes in a Jar for Gifting, and a Shelf-Life Chart")

ALTERNATES = [
    ("The Old-Fashioned Amish Dry Mix Pantry Cookbook",
     "150 Frugal Homemade Mixes and Meals from Scratch, with Baking, Soup and Seasoning "
     "Mixes, Gifts in a Jar, and a Shelf-Life Chart for Beginners"),
    ("The Amish Homemade Dry Mix Pantry Cookbook",
     "150 Simple Mixes in a Jar and Budget-Friendly Meals from Scratch to Stock Your "
     "Shelves, Save Money and Feed Your Family for Less"),
]

# Each chapter: (title, intro, [mixes], [recipes made with them])
# Chapter 10 is gift jars only.
CHAPTERS = [
    ("Biscuit & All-Purpose Baking Mixes",
     "The workhorse mixes of the Amish pantry: one scoop becomes biscuits, dumplings, pot pie toppings and quick suppers.",
     ["All-Purpose Amish Baking Mix", "Buttermilk Biscuit Mix", "Whole Wheat Baking Mix",
      "Drop Dumpling Mix", "Homemade Self-Rising Flour Blend"],
     ["Fluffy Amish Drop Biscuits", "Flaky Buttermilk Cut Biscuits", "Biscuits and Country Sausage Gravy",
      "Old-Fashioned Chicken and Dumplings", "Easy Crustless Ham and Cheese Pie", "Cheddar Garlic Biscuits",
      "Strawberry Shortcake Biscuits", "Chicken Pot Pie with Biscuit Topping", "Sausage Cheese Breakfast Bites",
      "Cinnamon Sugar Biscuit Bites"]),
    ("Pancake, Waffle & Breakfast Mixes",
     "Make-ahead mornings: stir in milk and eggs and breakfast is on the table in minutes.",
     ["Old-Fashioned Buttermilk Pancake Mix", "Whole Grain Oat Pancake Mix", "Crispy Waffle Mix",
      "Amish Baked Oatmeal Mix", "Maple Brown Sugar Instant Oatmeal Mix"],
     ["Fluffy Buttermilk Pancakes", "Blueberry Pancakes", "Apple Cinnamon Oat Pancakes", "Golden Crispy Waffles",
      "Sheet Pan Pancakes", "Amish Baked Oatmeal with Berries", "Peanut Butter Banana Baked Oatmeal",
      "Sausage Pancake Muffins", "Chocolate Chip Waffles", "Apple Pie Overnight Oats"]),
    ("Quick Bread, Muffin & Cornbread Mixes",
     "No yeast, no waiting: tender loaves, muffins and cornbread for breakfast, lunch boxes and supper.",
     ["Amish Cornbread Mix", "Basic Muffin Mix", "Amish Cinnamon Bread Mix (No Starter)",
      "Spiced Quick Bread Mix", "Bran Muffin Mix"],
     ["Skillet Cornbread", "Sweet Honey Corn Muffins", "Cornbread-Topped Chili Bake", "Blueberry Streusel Muffins",
      "Apple Cinnamon Muffins", "Amish Cinnamon Bread", "Classic Banana Bread", "Zucchini Bread",
      "Pumpkin Bread", "Morning Glory Bran Muffins"]),
    ("Cake, Brownie & Cookie Mixes",
     "Better-than-the-box desserts, from weeknight brownies to classic Amish whoopie pies.",
     ["Homemade Yellow Cake Mix", "Homemade Chocolate Cake Mix", "Fudgy Brownie Mix",
      "Soft Sugar Cookie Mix", "Oatmeal Cookie Mix"],
     ["Yellow Sheet Cake with Chocolate Frosting", "Chocolate Sheet Cake", "Cherry Dump Cake", "Fudgy Brownies",
      "Chewy Brownie Cookies", "Soft Amish Sugar Cookies", "Oatmeal Raisin Cookies", "Oatmeal Butterscotch Bars",
      "Yellow Cupcakes", "Amish Whoopie Pies"]),
    ("Yeast Bread & Roll Mixes",
     "Pre-measured bread mixes that take the guesswork out of homemade loaves, rolls and pizza night.",
     ["Amish White Bread Mix", "Honey Whole Wheat Bread Mix", "Soft Dinner Roll Mix",
      "Pizza Dough Mix", "Cinnamon Roll Mix"],
     ["Amish White Bread", "Honey Oat Wheat Bread", "Soft Amish Dinner Rolls", "Garlic Butter Knots",
      "Homemade Hamburger Buns", "Friday Night Pizza", "Ham and Cheese Stromboli", "Amish Cinnamon Rolls",
      "Soft Pretzels", "Pull-Apart Monkey Bread"]),
    ("Soup & Broth Base Mixes",
     "Replace cans and cubes with jars of homemade soup bases that cost pennies per serving.",
     ["Cream Soup Base Mix (Condensed Soup Substitute)", "Chicken-Style Bouillon Powder",
      "Beef-Style Bouillon Powder", "Homemade Onion Soup Mix", "Bean and Barley Soup Mix"],
     ["Cream of Chicken Soup", "Cream of Mushroom Soup", "Broccoli Cheddar Soup", "Amish Chicken Corn Soup",
      "Creamy Potato Soup", "French Onion Soup", "Savory Onion Pot Roast", "Hearty Bean and Barley Soup",
      "Vegetable Beef Soup", "Homestyle Chicken Noodle Soup"]),
    ("Gravy, Sauce & Casserole Base Mixes",
     "The secret to fast comfort food: shelf-stable gravies, sauces and stuffing ready for any casserole.",
     ["Brown Gravy Mix", "Country White Gravy Mix", "White Sauce Mix", "Cheese Sauce Mix",
      "Herb Bread Stuffing Mix"],
     ["Salisbury Steak with Brown Gravy", "Hot Roast Beef Sandwiches", "Chicken Fried Steak with Country Gravy",
      "Stovetop Mac and Cheese", "Cheesy Hamburger Skillet Pasta", "Tuna Noodle Casserole",
      "Amish Chicken and Stuffing Casserole", "Scalloped Potatoes", "Creamed Chipped Beef on Toast",
      "Amish Haystack Supper"]),
    ("Seasoning Blends & Dressing Mixes",
     "Big-batch spice blends and dressing mixes that turn plain chicken, beef and vegetables into family favorites.",
     ["Homemade Taco Seasoning", "Ranch Dressing and Dip Mix", "Italian Dressing Mix",
      "Seasoned Coating Mix for Oven-Baked Meats", "Amish Seasoning Salt"],
     ["Beef Taco Skillet", "Easy Taco Soup", "Creamy Ranch Dip", "Ranch Roasted Potatoes", "Crispy Oven-Baked Chicken",
      "Italian Pasta Salad", "Zesty Italian Chicken", "Seasoned Pork Chops", "Seasoned Oven Fries",
      "Homemade Seasoned Croutons"]),
    ("Hot Drink, Pudding & Sweet Treat Mixes",
     "Cozy drinks and simple desserts for cold evenings, church suppers and unexpected guests.",
     ["Creamy Hot Cocoa Mix", "Spiced Tea Mix", "Vanilla Pudding Mix", "Chocolate Pudding Mix",
      "Fruit Crisp Topping Mix"],
     ["Rich Hot Chocolate", "Peppermint Mocha", "Hot Spiced Tea", "Homemade Vanilla Pudding",
      "Old-Fashioned Banana Pudding", "Chocolate Pudding Pie", "Amish Apple Crisp", "Peach Crisp",
      "Mixed Berry Crisp", "Strawberry Rhubarb Crisp"]),
    ("Gifts in a Jar",
     "Layered mixes for holidays, teachers, neighbors and hostesses, each with ready-to-copy gift tag instructions.",
     [],
     ["Cowboy Cookies in a Jar", "Chocolate Chip Cookies in a Jar", "Brownies in a Jar",
      "Gingerbread Cookies in a Jar", "Snickerdoodles in a Jar", "Cranberry White Chip Oatmeal Cookies in a Jar",
      "Buttermilk Pancakes in a Jar", "Honey Cornbread in a Jar", "Friendship Soup in a Jar",
      "Chicken Noodle Soup in a Jar", "Nine-Bean Soup in a Jar", "Layered Hot Cocoa in a Jar",
      "Cappuccino Mix in a Jar", "Mulling Spices in a Jar", "Pumpkin Spice Bread in a Jar"]),
]

FRONT_MATTER = [
    ("Welcome to the Amish Pantry", "Why homemade mixes save money, time and trips to the store."),
    ("How to Use This Book", "The “one mix, many meals” system: each mix is followed by the recipes it makes."),
    ("Pantry Staples & Ingredients", "Flours, leaveners, powdered milk, powdered eggs, fats and spices: what to buy and why."),
    ("Jars, Tools & Containers", "Mason jars, airtight bins, oxygen absorbers, scoops and labels."),
    ("Storing Mixes Safely", "Cool, dry, dark storage; which mixes keep in the pantry and which belong in the fridge or freezer."),
]

BACK_MATTER = [
    ("Master Shelf-Life Chart", "Every mix in the book with its storage method and how long it keeps."),
    ("One Mix, Many Meals Index", "Find every recipe you can make from the mixes already on your shelf."),
    ("4-Week Pantry Meal Plan", "Breakfasts, suppers and desserts built from the book’s mixes."),
    ("Pantry Shopping List", "The bulk staples you need to make every mix in the book."),
    ("Kitchen Conversion Chart", "Cups, spoons, ounces, grams and oven temperatures."),
    ("Recipe Index", "All 150 recipes in alphabetical order."),
]

DESCRIPTION_HTML = """<p><b>Stock your pantry the old-fashioned Amish way, and turn one jar of homemade mix into breakfast, supper and dessert.</b></p>
<p>Store-bought mixes cost more than they should, and their labels are full of ingredients you can’t pronounce. Amish families have always done it differently. They blend their own flour, leavening, seasonings and spices in big batches, keep them on the pantry shelf, and scoop out exactly what they need on busy days.</p>
<p><i>The Complete Amish Dry Mix Pantry Cookbook</i> brings that simple, frugal kitchen wisdom into your home. It contains 150 recipes, each with a photo: 45 homemade dry mixes, 90 from-scratch meals and treats you can make with them, and 15 gifts in a jar.</p>
<p><b>Inside, you’ll find:</b></p>
<ul>
<li><b>45 shelf-stable pantry mixes:</b> all-purpose baking mix, pancake and waffle mixes, cornbread, cake and brownie mixes, bread and pizza dough mixes, cream soup base, gravy mixes, taco seasoning, ranch dressing mix, hot cocoa and more</li>
<li><b>90 easy recipes made with your mixes:</b> fluffy biscuits, chicken and dumplings, Amish baked oatmeal, whoopie pies, cinnamon rolls, chicken corn soup, Salisbury steak, Amish haystacks, fruit crisps and other family favorites</li>
<li><b>One mix, many meals:</b> each mix is followed by the recipes it makes, so you always know what to cook with what’s already on your shelf</li>
<li><b>15 gifts in a jar:</b> layered cookies, soups, breads and drinks with ready-to-copy gift tag instructions for holidays, teachers and neighbors</li>
<li><b>Clear, beginner-friendly instructions:</b> exact measurements, yields, storage containers and shelf life for every mix</li>
<li><b>Practical extras:</b> a master shelf-life chart, a mix-to-meal index, a 4-week pantry meal plan, a pantry shopping list and a kitchen conversion chart</li>
</ul>
<p><b>Why home cooks love dry mixes:</b></p>
<ul>
<li><b>Save money:</b> homemade mixes cost a fraction of boxed versions</li>
<li><b>Know what’s in your food:</b> no preservatives, fillers or hidden additives</li>
<li><b>Save time:</b> do the measuring once and enjoy from-scratch meals all month</li>
<li><b>Be ready for anything:</b> a well-stocked pantry means fewer trips to the store</li>
</ul>
<p>Whether you’re new to homemade mixes, building a homestead pantry or looking for thoughtful handmade gifts, this book gives you everything you need to fill your shelves with jars that turn into real home cooking.</p>
<p><b>Start your Amish pantry today.</b></p>"""
