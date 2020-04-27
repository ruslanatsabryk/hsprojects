package bot

import java.util.*
import kotlin.test.assertTrue


val scanner = Scanner(System.`in`) // Do not change this line

fun main() {
    greet("Aid", "2020") // change it as you need
    remindName()
    guessAge()
    count()
    test()
    end()
}

fun greet(assistantName: String, birthYear: String) {
    println("Hello! My name is " + assistantName + ".")
    println("I was created in " + birthYear + ".")
    println("Please, remind me your name.")
}

fun remindName() {
    val name = scanner.nextLine()
    println("What a great name you have, " + name + "!")
}

fun guessAge() {
    println("Let me guess your age.")
    println("Say me remainders of dividing your age by 3, 5 and 7.")
    val rem3 = scanner.nextInt()
    val rem5 = scanner.nextInt()
    val rem7 = scanner.nextInt()
    val age = (rem3 * 70 + rem5 * 21 + rem7 * 15) % 105
    println("Your age is " + age + "; that's a good time to start programming!")
}

fun count() {
    println("Now I will prove to you that I can count to any number you want.")
    val num = scanner.nextInt()
    for (i in 0..num) {
        print(i)
        println("!")
    }
}

fun test(): Boolean {
    println("Let's test your programming knowledge.")
    println("What is AGE++?")
    println("1. I do not care.")
    println("2. This is a new programming language instead of C++.")
    println("3. The name of the drug to prolong life.")
    println("4. This is a programmer's birthday.")
    var answer = scanner.nextInt()
    if (answer != 4) {
        println("Please, try again.")
        answer = scanner.nextInt()
    }
    if (answer != 0) {
        return true
    }
    return false

}

fun end() {
    println("Congratulations, have a nice day!") // Do not change this text
}