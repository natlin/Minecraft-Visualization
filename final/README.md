Minecraft Data Visualization
============================

Team Members
------------
Nathan Lin - 100% of work


Resources
---------
This project used these particuar resources:
* http://bl.ocks.org/kerryrodden/7090426
* http://bost.ocks.org/mike/miserables/
* http://stackoverflow.com/questions/20463614/les-miserables-co-occurrence
* http://bl.ocks.org/mbostock/4349545

Referenced Libraries
--------------------
jQuery
* This was used for functions to set the default select options for drop down menus

D3
* This was used for basically all the visualization

Explanation
===========

index.html
----------
This view is the main page. This shows an overview of the entire dataset. There is a sequence sunburst that displays the actions taken. The inner circle depicts the different servers, and the outer circle depicts the 8 actions (KilledBy, Logins, Chat, Death, CraftedItems, Kicks, BlockPlace, BlockBreak). A percentage will be shown inside the circle depicted the percentage of that particular action in relation to every action. This percentage will also show up on the breadcrumb trail, located in the upper left. This will show the name of the server and the name of the action, along with a percentage. The sunburst is color coded and you can see all the different colors and what they stand for by clicking on the Legend button in the upper right, which will show the legend. Two buttons are also on the page which will bring you to the other two views. Note, the data used does not take into account the Count variable, because the Count for BlockBreak and BlockPlace is so huge that the data would be extremely skewed and thus you would only see those two actions on the sunburst since the other actions do not nearly have enough count instances. Instead, my sequence sunburst takes into account only the amount of entries in the dataset, instead of amount of entries * count.

killslider.html
---------------
This view shows the amount of kills per server that occur. This data DOES include the count variable. There is a slider, which allows the user to specify the time range in which they want to see the amount of kills. The x-axis is time and the y-axis is the server. Note that there is nothing on y=8 since the 8th server had 0 KilledBy entries. The circles represent the KilledBy data. The larger the circle, the more player kills occured during that specific time. There is a drop down menu that allows the user to select which server they would like to look at the data for, as well as an option to select all servers to view total player kills across all servers. Two buttons are also on the page which will bring you to the other two views.

chat.html
---------
This view shows player-player interaction through chat. There is a matrix which shows the interactions between servers. Note that there is always a diagonal line, since each player will always interact with itself. The matrix has colored squares when the player has chatted with another player. The darker the color of the square, the more times that Player A has interacted with Player B. When the mouse is hovered over a square of the matrix, the names of the people involved in that interaction will be displayed in red. You can order the matrix through a drop down menu which allows you to sort alphabetically by name, or by the count of how many times the player has chatted. There is another drop down menu which allows you to select which server to view the interactions with. This only shows the interactions of 70 players (71 in the case of Server 11) since there are so many different players on each server, that there would not be enough space on the screen to display the interactions between all players.

Conclusions
===========

Insights
--------
Some insights that cannot be gleamed from the dataset alone:
* Not all servers have equal amounts of players. Some servers are a lot more popular than other servers
* Not all servers have all actions occur. Some do not have any player kills, some do not have any crafted items, etc
* Something interesting was that Server 8 had zero player kills, yet it had a lot more players than Server 3. It is interesting that even with more people, they did not have anyone that turned into a player killer.

Extra Credit
------------
* Among the extra credit tasks, one of the examples was saying to show which server was the bloodiest. The killslider.html can display this by the size of the circles on the visualization.
* Player activity across servers can be seen in the index.html overview, as you can see the percentage of actions on each server based on the size of the arcs. You can see that certain servers have more BlockPlace while others have more KilledBy, etc.
