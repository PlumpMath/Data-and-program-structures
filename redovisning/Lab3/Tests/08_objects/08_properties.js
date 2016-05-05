var pile = {
  elements: ["eggshell", "orange peel", "worm"],
  get height() {
    return this.elements.length;
  },
  set value(value) {
    this.elements.push(value)
  }
}

console.log(pile.height)
console.log(pile.value = "can")
console.log(pile.height)
