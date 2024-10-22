// Literal class representing a single term of the polynomial
class Literal {
    double coefficient;
    int exponent;
    Literal next; // Reference to the next node in the linked list

    // Constructor for the Literal class
    public Literal(double coef, int exp) {
        this.coefficient = coef;
        this.exponent = exp;
        this.next = null;
    }

    // Accessor methods (getters)
    public double getCoefficient() {
        return coefficient;
    }

    public int getExponent() {
        return exponent;
    }
}

// Polynomial class with extra credit functionalities
public class Polynomial {
    private Literal head;

    // Constructor to initialize an empty polynomial
    public Polynomial() {
        head = null;
    }

    // Insert a term into the polynomial in sorted order (by exponent)
    public void insertTerm(double coef, int exp) {
        Literal newTerm = new Literal(coef, exp);

        if (head == null || head.exponent < exp) {
            newTerm.next = head;
            head = newTerm;
            return;
        }

        Literal current = head;
        while (current.next != null && current.next.exponent > exp) {
            current = current.next;
        }

        if (current.exponent == exp) {
            current.coefficient += coef;
        } else {
            newTerm.next = current.next;
            current.next = newTerm;
        }
    }

    // Method to add two polynomials
    public Polynomial add(Polynomial rhs) {
        Polynomial result = new Polynomial();
        Literal p1 = this.head;
        Literal p2 = rhs.head;

        while (p1 != null || p2 != null) {
            if (p1 == null) {
                result.insertTerm(p2.coefficient, p2.exponent);
                p2 = p2.next;
            } else if (p2 == null) {
                result.insertTerm(p1.coefficient, p1.exponent);
                p1 = p1.next;
            } else if (p1.exponent > p2.exponent) {
                result.insertTerm(p1.coefficient, p1.exponent);
                p1 = p1.next;
            } else if (p1.exponent < p2.exponent) {
                result.insertTerm(p2.coefficient, p2.exponent);
                p2 = p2.next;
            } else {
                result.insertTerm(p1.coefficient + p2.coefficient, p1.exponent);
                p1 = p1.next;
                p2 = p2.next;
            }
        }

        return result;
    }

    // Method to multiply two polynomials
    public Polynomial multiply(Polynomial rhs) {
        Polynomial result = new Polynomial();
        for (Literal p1 = this.head; p1 != null; p1 = p1.next) {
            Polynomial temp = new Polynomial();
            for (Literal p2 = rhs.head; p2 != null; p2 = p2.next) {
                temp.insertTerm(p1.coefficient * p2.coefficient, p1.exponent + p2.exponent);
            }
            result = result.add(temp);
        }
        return result;
    }

    // Parse the input string to handle polynomials without spaces and unary operators
    public static Polynomial parsePolynomial(String input) {
        Polynomial polynomial = new Polynomial();
        Stack<Double> coefficients = new Stack<>();
        Stack<Integer> exponents = new Stack<>();
        Stack<Character> operators = new Stack<>();

        StringBuilder currentNum = new StringBuilder();
        boolean isExponent = false;
        char lastOperator = '+';

        for (int i = 0; i < input.length(); i++) {
            char c = input.charAt(i);

            if (Character.isDigit(c) || c == '.') {
                currentNum.append(c);
            } else if (c == 'x') {
                coefficients.push(parseCoefficient(currentNum.toString(), lastOperator));
                currentNum = new StringBuilder();
                isExponent = true;
            } else if (c == '^') {
                if (isExponent) {
                    exponents.push(Integer.parseInt(currentNum.toString()));
                    currentNum = new StringBuilder();
                    isExponent = false;
                }
            } else if (c == '%') {
                double lastCoefficient = coefficients.pop();
                lastCoefficient %= Integer.parseInt(currentNum.toString());
                coefficients.push(lastCoefficient);
                currentNum = new StringBuilder();
            } else {
                if (c == '+' || c == '-') {
                    lastOperator = c;
                }
                if (currentNum.length() > 0) {
                    if (isExponent) {
                        exponents.push(Integer.parseInt(currentNum.toString()));
                    } else {
                        coefficients.push(parseCoefficient(currentNum.toString(), lastOperator));
                        exponents.push(0); // No exponent means x^0 (constant term)
                    }
                    currentNum = new StringBuilder();
                }
            }
        }

        // Add the remaining term
        if (currentNum.length() > 0) {
            if (isExponent) {
                exponents.push(Integer.parseInt(currentNum.toString()));
            } else {
                coefficients.push(parseCoefficient(currentNum.toString(), lastOperator));
                exponents.push(0); // Constant term
            }
        }

        while (!coefficients.isEmpty() && !exponents.isEmpty()) {
            polynomial.insertTerm(coefficients.pop(), exponents.pop());
        }

        return polynomial;
    }

    // Method to parse coefficient considering the unary + or - operator
    private static double parseCoefficient(String num, char operator) {
        double value = Double.parseDouble(num);
        return operator == '-' ? -value : value;
    }

    // Method to represent the polynomial as a string
    public String toString() {
        if (head == null) {
            return "0";
        }

        StringBuilder sb = new StringBuilder();
        Literal current = head;
        while (current != null) {
            if (current.coefficient > 0 && current != head) {
                sb.append("+");
            }
            sb.append(current.coefficient).append("x^").append(current.exponent).append(" ");
            current = current.next;
        }

        return sb.toString().trim();
    }

    // Testing the Polynomial functionality
    public static void main(String[] args) {
        // Parse polynomials with extra credit features
        Polynomial poly1 = Polynomial.parsePolynomial("3x^4+5x^2+1");
        Polynomial poly2 = Polynomial.parsePolynomial("2x^3+4x^2+6");

        System.out.println("Polynomial 1: " + poly1);
        System.out.println("Polynomial 2: " + poly2);

        // Test addition
        Polynomial sum = poly1.add(poly2);
        System.out.println("Sum: " + sum);

        // Test multiplication
        Polynomial product = poly1.multiply(poly2);
        System.out.println("Product: " + product);

        // Test parsing with modulo and exponentiation
        Polynomial poly3 = Polynomial.parsePolynomial("2+3*5%2");
        System.out.println("Parsed Poly3 (with modulo): " + poly3);
    }
}
