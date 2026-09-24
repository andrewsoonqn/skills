## Stage 2: Validate user input

### Question

We are trying to stop the form from submitting when the email address is empty or invalid.

How can we do this?

<details>
<summary>High-level prompt</summary>

Add email validation to the form submission handler. Invalid input must return an error. Valid input must submit the form.

</details>

<details>
<summary>Implementation steps</summary>

1. Read the email value.
2. Check whether it has a valid format.
3. Return an error if the check fails.
4. Submit the form if the check passes.

</details>

<details>
<summary>Code skeleton</summary>

```ts
function handleSubmit(email: string) {
  // Check the email format.
  // Return an error when the check fails.
  // Submit the form.
}
```

</details>

<details>
<summary>Complete code</summary>

```ts
function handleSubmit(email: string) {
  const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  if (!isValid) {
    return { error: "Enter a valid email address." };
  }

  return submitForm({ email });
}
```

</details>

### Check your work

Test these values:

1. An empty string
2. `andrew`
3. `andrew@example.com`

The first two values must return an error. The third must call `submitForm`.

After you finish, come back with:

- Your implementation
- The test results
- Any part you did not understand
