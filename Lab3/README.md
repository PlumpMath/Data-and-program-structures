To run one test, do:

```
./es.py ./Tests/01_literals.js
```


In order to run one test and compare its outputs to the expected outputs, run:

```
./espytester.py ./es.py ./ 01_literals
```

Note how 01_literals is the name a file inside the Tests folder. So in order to run the tests in 02_expressions/01_addition.js we execute:

```
./espytester.py ./es.py ./ 02_expressions/01_addition
```

To run all tests:

```
./espytester.py ./es.py ./
```



Current:

./espytester.py ./es.py ./ 03_variables/01_definition
