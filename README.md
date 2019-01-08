## Battleship


Class: Programming Languages 220

Date: 9/23/2015 sophomore year

Program Name: ASCII Battleship Clone

Programmers: Bjorn Mathisen and Jacob Huss

A battleship clone game, the end goal is for either the player or the AI/computer
to destroy all the ships on the opposing team. They can accomplish this with a 
varriety of artillary, including bombs, torpedoes, and single hit missiles. The 
AI is programmed to select random coordinates and on occasion use a limited supply
of artillary, the same amount is alloted to the player. For deployment purposes
the player can select either manual or automatic deployment, the computers ships
are always randomly automatically assigned positions. When the player places his
ships he has the option to place them left, right, up or down. Error checking 
validates these coordinates before placing a ship. To view the players/enemy board
a algorithm was designed that would allow the programming to view the map as values
and the player would see appropriate symbols depending on the ship and the damage
that each ship has sustained. 

### Board Game Symbol Definition List
| Name | HP | Short Name |
|------|----|------------|
|Carrier|5|C
|Battleship|4|B
|Destroyer|3|D
|Submarine|2|S

| Function                        | Base String	| Player View (Own Board) |		Player View (Enemy Board) |
|---------------------------------|-------------|-------------------------|-----------------------------|
| Empty space, not fired on	      | "0"					|  " "		                |	"?"
| Empty space, missed shot				| "1"				  |  "*"						        | " "
| Carrier, not fired on					  | "2"					|  "C"						        | "?"
| Carrier, fired on, not sunk			| "3"					|  "X"						        | "X"
| Carrier, fired on, sunk				  | "4"					|  "X"						        | "C"	
| Battleship, not fired on				| "5"					|  "B"						        | "?"
| Battleship, fired on, not sunk	|	"6"					|  "X"						        | "X"
| Battleship, fired on, sunk			| "7"					|  "X"						        | "B"
| Destroyer, not fired on				  | "8"					|  "D"						        | "?"
| Destroyer, fired on, not sunk		| "9"					|  "X"						        | "X"
| Destroyer, fired on, sunk				| "A"					|  "X"						        | "D"
| Submarine, not fired on				  | "B"					|  "S"						        | "?"
| Submarine, fired on, not sunk		| "C"					|  "X"						        | "X"
| Submarine, fired on, sunk				| "D"					|  "X"						        | "S"
