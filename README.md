![Logo](https://user-images.githubusercontent.com/39225800/167252965-b0515923-5785-47e8-8fef-ab045606f035.png)

# Auto Elytra Evolution
An evolutionary algorithm that learns to break physics (in Minecraft) and fly indefinetly without the need of rockets. 🚀

## Description
The project is created in tandem with the [Auto Elytra](https://github.com/MarkasAis/auto-elytra) Minecraft Client-Side Mod that gives you **autonomous** flying in any *Multiplayer/Singleplayer* world.

This project emulates exact Minecraft flying physics and runs an evolutionary algorithm to optimize parameters that are then used to control the player.
The evolved parameters are then used by the Minecraft Mod to run the flying algorithm in-game.

![Preview](https://user-images.githubusercontent.com/39225800/167252636-de95fe68-9271-4827-8bcc-34933d710330.png)  
*(Player trajectories are plotted to see progress)*

## 🛠️ Technical Details
### Multiplayer Support
There is a quirk with Minecraft Multiplayers servers where if a player moves too fast with an elytra their velocity gets reset to 0 (not quite sure why, maybe slow chunk loading). Obviously this is not beneficial for an algorithm that uses momentum to achieve infinite flight. My physics emulator implements a speed threshold (that I've found by experimentation) so that the agents learn a flying pattern that is viable for Multiplayer servers.

### Scoring Function
I have experimented with different scoring functions, and the one that I've found to work best is the slope of a **Simple Linear Regression** of the player's trajectory.  

This way the agents that need to fly downwards to gain momentum and get back up are not discriminated over early local maximum strategies such as "glide horizontaly and slowly lose elevation".



