# How to use AgentScript scriptcc

use the provided `grounds-assembly-X.Y.Z.jar` to load the jason file of the project.

This benchmark also uses an extra dummy package that "generates" colors for the chameneos based on their number. The package is provided in `waiting_actions.jar`

to run this benchmark run 

```bash
$ java -cp "grounds-assembly-0.1.0-SNAPSHOT.jar:./ping_pong/agentscript/waiting_actions.jar" scriptcc.Main ./ping_pong/agentscript/input.json
```

> change the `:` to `;` for windows environments
