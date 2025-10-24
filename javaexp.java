import java.util.Scanner;

public class Stack {
    private int[] arr;
    private int top = -1;

    // Constructor to set size
    public Stack(int size) {
        arr = new int[size];
    }

    public boolean isEmpty() {
        return top == -1;
    }

    public boolean isFull() {
        return top == arr.length - 1;
    }

    public void push(int value) {
        if (isFull()) {
            System.out.println("Stack is full");
        } else {
            arr[++top] = value;
            System.out.println("Pushed " + value);
        }
    }

    public int pop() {
        if (isEmpty()) {
            System.out.println("Stack underflow");
            return -1;
        } else {
            return arr[top--];
        }
    }

    public int peek() {
        if (isEmpty()) {
            System.out.println("Stack is empty");
            return -1;
        } else {
            return arr[top];
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter stack size: ");
        Stack stack = new Stack(sc.nextInt());

        // Demonstration:
        stack.push(10);
        stack.push(20);
        System.out.println("Top is: " + stack.peek());
        System.out.println("Popped: " + stack.pop());
        System.out.println("Is empty? " + stack.isEmpty());
        sc.close();
    }
}
