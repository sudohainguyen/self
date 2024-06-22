use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::io::{self, Write};

type Db = Arc<Mutex<HashMap<String, String>>>;

struct KvStore {
    db: Db,
}

impl KvStore {
    fn new() -> Self {
        KvStore {
            db: Arc::new(Mutex::new(HashMap::new())),
        }
    }

    fn set(&self, key: String, value: String) {
        let mut db = self.db.lock().unwrap();
        db.insert(key, value);
    }

    fn get(&self, key: String) -> Option<String> {
        let db = self.db.lock().unwrap();
        db.get(&key).cloned()
    }

    fn delete(&self, key: String) -> Option<String> {
        let mut db = self.db.lock().unwrap();
        db.remove(&key)
    }
}

fn main() {
    let store = KvStore::new();
    loop {
        print!("> ");
        io::stdout().flush().unwrap();
        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();
        let parts: Vec<&str> = input.trim().split_whitespace().collect();
        if parts.is_empty() {
            continue;
        }
        match parts[0] {
            "set" if parts.len() == 3 => {
                store.set(parts[1].to_string(), parts[2].to_string());
                println!("OK");
            }
            "get" if parts.len() == 2 => {
                match store.get(parts[1].to_string()) {
                    Some(value) => println!("{}", value),
                    None => println!("Key not found"),
                }
            }
            "delete" if parts.len() == 2 => {
                match store.delete(parts[1].to_string()) {
                    Some(_) => println!("OK"),
                    None => println!("Key not found"),
                }
            }
            "exit" => break,
            _ => println!("Unknown command"),
        }
    }
}