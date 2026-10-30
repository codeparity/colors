#[derive(Debug)]
struct Theme {
    name: &'static str,
    background: &'static str,
}

fn main() {
    let theme = Theme { name: "CodeParity", background: "#202124" };
    println!("{} on {}", theme.name, theme.background);
}
