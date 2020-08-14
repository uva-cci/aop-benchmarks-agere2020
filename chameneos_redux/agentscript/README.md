# How to use AgentScript scriptcc

use the provided `grounds-assembly-X.Y.Z.jar` to load the jason file of the project.

This benchmark also uses an extra dummy package that "generates" colors for the chameneos based on their number. The package is provided in `cham_data_test-1.0.jar`

to run this benchmark run 

```bash
$ java -cp "grounds-assembly-0.1.0-SNAPSHOT.jar:./chameneos_redux/source_files/agentscript/cham_data_test-1.0.jar" scriptcc.Main ./chameneos_redux/source_files/agentscript/input.json
```

> change the `:` to `;` for windows environments
