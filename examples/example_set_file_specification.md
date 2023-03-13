# Example Set File Specification
----

## Example sets consists of two types of statements:

- Domain statements:

  ```
  d [num_attrs] [attr_1_domain_size] [attr_2_domain_size] ... [attr_n_domain_size]
  ```

  *There should only be one domain statement per example set file.*

- Example statements:

  ```
  e [alt1] [alt2] [relation] [agent]
  ```

### Description of variables:

| Variable           | Description                                       |
|--------------------|---------------------------------------------------|
| num_attrs          | The number of attributes.                         |
| attr_i_domain_size | The size of the i<sup>th</sup> attribute's domain |
| alt1               | The first alternative in the example.             |
| alt2               | The second alternative in the example.            |
| relation           | The relations between alt1 and alt2.              |
| agent              | The id of the agent which generated the example.  |

Alternatives are described by a comma separated string of integers, one for each attribute value.

Relations are described as follows:

| Value | Relation                               |
|-------|----------------------------------------|
|  -3   | alt2 is incomparable with alt1. [^1]   |  
|  -2   | alt2 is strictly preferred to alt1.    |
|  -1   | alt2 is at least as preferred as alt1. |
|   0   | alt1 is equally preferred to alt2.     |
|   1   | alt1 is at least as preferred as alt2. |
|   2   | alt1 is strictly preferred to alt2.    |
|   3   | alt1 is incomparable with alt2.        |

[^1]: Conventionally -3 will not occur as it is identical to 3, but may be useful in some contexts.
