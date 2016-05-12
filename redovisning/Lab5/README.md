We made one semantic modification to the tests:

-- self.assertEqual(stack[0].args, args)
++ self.assertEqual(stack[0].argNames, args)

Detta var eftersom vår Function hade argumenten under namnet argNames istället för args - och vi visste inte vid tillfället huruvida vi var godkända på Lab 3 och tänkte att det skulle skapa kaos att synkronisera förändringar från olika källor i SVN-repot.

To run all tests:

```
./run_tests
```
