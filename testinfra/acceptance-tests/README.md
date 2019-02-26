# Maintenance Updates testing

This a draft on how we can automate the testing of fixes and
features. We can't avoid manual testing but we can automate a lot.

The idea is to write the test suite when we are working on a bug.

The tests are based on [pytest](https://docs.pytest.org/en/latest/)
which mostly relies on [Testinfra](https://testinfra.readthedocs.io/en/latest/)
for acceptance/integration testing.

## Structure


## Tests

For each bug, create the test functions in the concerned files.

Add a marker with the `bsc` for each function.

```python
pytest.mark.bsc1234567
```

## Run the tests manually

The parts 1 and 2 should be done in automation.

1. Generate environment.json
2. Generate environment.ssh_config

3. Test all

```console
./testAllRoles.sh $ENVIRONMENT $SSH_CONFIG ../bsc-tests/S-M-10303-184108/ -v
```

3. Test only a specific bug

e.g with pytest, this would need to be integrated in a proper way for CI

```console
py.test --connection ssh --sudo --hosts 10.84.154.105 -m "bsc1234567"  -v
```
