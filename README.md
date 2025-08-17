

![wheel](https://github.com/user-attachments/assets/eb2865fa-43ce-484a-b56a-4a24f5d4f873)

#  Tektõn

This project introduces an algebraic model for computational psychology named Tektōn, where personality and cognition are represented as functional elements using specific mathematical operations and relationships. This README provides an overview of the syntax, rules, and operations for manipulating these elements within the model.

---
## Table of Contents
- [Introduction](#introduction)
- [The Algebraic Language of Cognition](#the-algebraic-language-of-cognition)
  - [Cognitive Functions & Properties](#cognitive-functions--properties)
  - [Operators & Syntax](#operators--syntax)
  - [Priority & Transformation Rules](#priority--transformation-rules)
- [Astrological & Elemental Correspondence](#astrological--elemental-correspondence)
- [Usage Examples](#usage-examples)
- [Contributors](#contributors)

---

## Introduction
This model aims to describe elements of personality and cognition using algebraic rules. Functions representing dimensions of personality and cognitive processes can interact, combine, and influence each other through defined operations. These operations and rules simulate complex psychological dynamics and provide insights into cognitive processes and personality traits through mathematical notation.

## The Algebraic Language of Cognition

This system models cognitive dynamics. You must adhere strictly to its syntax and rules.

### Cognitive Functions & Properties

| Symbol | Name                  | Density        | Charge | Dimension |
| :----: | :-------------------- | :------------- | :----: | :-------: |
|  `Si`  | Introverted Sensing   | Very Dense     |   i    |     S     |
|  `Ni`  | Introverted Intuition | Very Dense     |   i    |     N     |
|  `Ne`  | Extraverted Intuition | Dense          |   e    |     N     |
|  `Fi`  | Introverted Feeling   | Dense          |   i    |     F     |
|  `Te`  | Extraverted Thinking  | Somewhat Light |   e    |     T     |
|  `Fe`  | Extraverted Feeling   | Somewhat Light |   e    |     F     |
|  `Ti`  | Introverted Thinking  | Light          |   i    |     T     |
|  `Se`  | Extraverted Sensing   | Very Light     |   e    |     S     |

### Operators & Syntax

- **Grouping `( )`**: Parentheses group terms for isolated operations. e.g., `(Se ~ Ti)`.
- **Combination `+`**: Combines separate terms.
- **Coefficients**:
  - A number preceding a function denotes its **mass**. (e.g., `5Si`).
  - A number outside parentheses denotes **acceleration** and does not affect internal mass. (e.g., `40(...)`).

- **Top `~`**: The 'right operator'. Describes a relationship where a T/F function orbits an S/N function (or vice versa). In this operation, the primary operand is compartmentalized into "chunks" of action or judging categorization by the second operand, bringing order to it and creating a drag.

- **Right `→`**: The 'drag' operator. Represents a function pulling an opposite-charge and opposite-domain function. This is a retroactive mechanism where a function becomes its opposite by reacting with other functions, but maintains a link to its previous state.

- **Left `oo`**: The 'opposition' operator. Subtracts functions of the same domain but different charges, resulting in a Right/Drag (`→`) expression.

- **Bottom `|`**: The 'non-interaction' operator. Indicates two terms cannot react but dynamically switch between each other, taking turns to manifest.

### Priority & Transformation Rules

1.  **Addition**: First, combine like functions across terms by adding their mass coefficients.
    - Example: `(2Se) + (3Se) = (5Se)`
2.  **Opposition First**: Always resolve opposition (`oo`) operations before others, as they generate new drag reactions.
3.  **Drag Creation**: A drag (`→`) reaction is created under two conditions:
    - By opposing two functions: `7Se oo 5Si = 2Se → Ni`
    - By orbiting two functions of opposite dimension: `7Se ~ 3Ti = 4Se → Ni`
4.  **Drag Accumulation**: Within a single term, drag reactions in the same domain accumulate until only one remains.
5.  **Subtraction with Drag**: When using `oo` or `~`, the function with the higher mass "carries" the difference and dictates the resulting drag.
    - Example: `7Se oo 5Si = 2Se → Ni`
6.  **Orbital Drag Creation**: An orbital relationship (`~`) between a sensory (S/N) and a judgment (T/F) function always creates a drag. The more massive function dictates the nature of the drag.
    *   `Si ~ Te` results in a drag involving `Ne`.
    *   `Te ~ Si` results in a drag involving `Fi`.

#### Opposition (`oo`) Examples Table

The following table lists common outcomes for the opposition operator (`oo`). The function with the higher coefficient carries the drag to the opposite dimension and charge.

| Expression      | Result           | Reasoning                             |
|-----------------|------------------|---------------------------------------|
| `2Se oo Si`     | `Se → Ni`        | `Se` is higher, carries the drag      |
| `2Si oo Se`     | `Si → Ne`        | `Si` is higher, becomes the carrier   |
| `2Ne oo Ni`     | `Ne → Si`        | `Ne` is higher, carries the drag      |
| `2Ni oo Ne`     | `Ni → Se`        | `Ni` is higher, becomes the carrier   |
| `2Te oo Ti`     | `Te → Fi`        | `Te` is higher, carries the drag      |
| `2Ti oo Te`     | `Ti → Fe`        | `Ti` is higher, becomes the carrier   |
| `2Fe oo Fi`     | `Fe → Ti`        | `Fe` is higher, carries the drag      |
| `3Fi oo 2Fe`    | `Fi → Te`        | `Fi` is higher, carries the drag      |

---
## Astrological & Elemental Correspondence

Use the following table to map the final, simplified algebraic expressions to their astrological and elemental counterparts.

| Astrological Placement | Elemental Name          | Algebraic Expression                          |
| :--------------------- | :---------------------- | :-------------------------------------------- |
| Aries-Pisces           | Explosion               | `Se ~ Fi`                                     |
| Aries-Aries            | Lacerate                | `Se`                                          |
| Aries-Taurus           | Cut                     | `(Se ~ Fi) oo Si`                             |
| Taurus-Aries           | Hit/Strike              | `((Si ~ Fe) oo Se)`                           |
| Taurus-Taurus          | Rock                    | `((Si oo Se) -> Ne )`                          |
| Taurus-Gemini          | Dust                    | `Ne -> (Si ~ Fe)`                             |
| Gemini-Taurus          | Quartz                  | `((Ne oo Ni) -> Se) ~ Fe`                      |
| Gemini-Gemini          | Echoes                  | `(Ne ~ Fe)`                                   |
| Gemini-Cancer          | Whispers                | `( (Ne -> Si) ~ Ti | Se ~ Fi)`                |
| Cancer-Gemini          | Rain                    | `(Ne ~ Fi | Se ~ Ti)`                         |
| Cancer-Cancer          | River                   | `~ (Fe oo Fi)`                                |
| Cancer-Leo             | Roots                   | `(Fi oo Fe) ~ Si`                             |
| Leo-Cancer             | Trunk                   | `(Fi -> Te) ~ (Si oo Se)`                     |
| Leo-Leo                | Light                   | `Te ~ Ni`                                     |
| Leo-Virgo              | Thunder                 | `(Te ~ Se | Fe ~ Ne)`                         |
| Virgo-Leo              | Carbonization           | `(Si ~ Te | Ni ~ Fe)`                         |
| Virgo-Virgo            | Filtration              | `Si ~ (Te oo Ti)`                             |
| Virgo-Libra            | Crystal                 | `Si ~ (Fe oo Fi)`                             |
| Libra-Virgo            | Rhythm                  | `(Fe ~ Si | Te ~ Ni )`                         |
| Libra-Libra            | Wind                    | `(Fi oo Fe) ~`                                |
| Libra-Scorpio          | Hail                    | `(Fe oo Fi) ~ Ni`                             |
| Scorpio-Libra          | Ice                     | `(Se -> Ni) ~ (Fe oo Fi)`                     |
| Scorpio-Scorpio        | Phoenix                 | `(Ni -> Se) ~ Te`                             |
| Scorpio-Sagittarius    | Poison                  | `(Se ~ Fi | Ne ~ Ti)`                         |
| Sagittarius-Scorpio    | Pierce/Drill            | `Ni ~ (Te -> Fi)`                             |
| Sagittarius-Sagittarius| Fire/Blaze              | `(Se ~ Te | Ne ~ Fe)`                         |
| Sagittarius-Capricorn  | Meteor                  | `Ni ~ (Ti -> Fe)`                             |
| Capricorn-Sagittarius  | Gravity                 | `( Ne ~ Ti | Se ~ Fi)`                         |
| Capricorn-Capricorn    | Friction                | `(Te oo Ti) ~`                                |
| Capricorn-Aquarius     | Darkness                | `(Ti oo Te) ~ Ni`                             |
| Aquarius-Capricorn     | Static                  | `(Fi -> (Te oo Ti))`                          |
| Aquarius-Aquarius      | Greatsword/Cleave       | `(Fe -> Ti) ~ Ne`                             |
| Aquarius-Pisces        | Shadows                 | `(Ti ~ Ne | Fi ~ Se)`                         |
| Pisces-Aquarius        | Ghost                   | `( Fi ~ Se | Ti ~ Ne)`                         |
| Pisces-Pisces          | Void/Vacuum             | `Ne ~ Fi`                                     |
| Pisces-Aries           | Lightning               | `(Fi ~ Ne | Ti ~ Se)`                         |

---

## Usage Examples

*Note: These examples follow the core principles of the language. Refer to the updated rules for detailed transformation logic.*

### Example 1: Solving a Complex Reactor
```text
Reactor = 40(5Se ~ 3Ti) + 9(8Ni → 3Se ) + 10( 2Se ~ 2Se oo 3Si)

Step-by-Step Solution:
1. Sum all instances of `Se` as it's the most common.
   Result: `51(10Se ~ 3Ti → 8Ni) + 8(2Ne → Si)`

2. Carry `Ni` by the largest `Se` function, adjusting acceleration.
   Result: `59(10Se ~ 3Ti → 8Ni oo 2Ne → Si)`

3. Prioritize subtraction (`oo`) to create a drag.
   Result: `59(10Se ~ 3Ti → 6Ni → 2Se oo Si)`

4. Final result after reduction:
   Result: `59(11Se ~ 3Ti → 9Ni)`


2(Te ~ Si) | 4(Fe ~ Ni) + (2Ne oo Ni) + 4(Se)

Solution Steps:

1. Solve reduction (`oo`).
2. Convert reductions and remove the `|` operator.
   Result: `2(Te ~ Si) + 4(Fe ~ 4Se → Ni)`

3. Complete reduction with final adjustment:
   Result: `6(Te ~ Si oo 4Se → Ni)`

Final simplified expression:
   `6(Te ~ 3Se → 2Ni)`
