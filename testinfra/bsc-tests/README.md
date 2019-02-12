# Maintenance Updates testing

This a draft on how we can automate the testing of fixes and
features. We can't avoid manual testing but we can automate a lot.

The idea is to write the test suite when we are working on a bug.

The tests are based on [pytest](https://docs.pytest.org/en/latest/)
which mostly relies on [Testinfra](https://testinfra.readthedocs.io/en/latest/)
for acceptance/integration testing.

## Structure

* When there is no MU

Put the test file in `waiting_for_mu`

* When a MU is ready

Create a directory for the test files regarding a MU:

`S-M-10303-184108`

**S**: Suse

**M**: Maintenance

**10303**: MR - Maintenance Request

**184108**: RR - Release Request


## Tests

Create a test suite in the MU directory: 

* at the beginning of the file, add the title and link
to the relative PR(s)


## Run the tests manually

The parts 1 and 2 should be done in automation.

1. Generate environment.json
2. Generate environment.ssh_config
3. Test

example:

```console
./testAllRoles.sh $ENVIRONMENT $SSH_CONFIG ../bsc-tests/S-M-10303-184108/ -v
```
