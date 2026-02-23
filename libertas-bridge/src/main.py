from libertas_shield.shield import SovereignShield

def main():
    shield = SovereignShield()
    print("\n" + "="*60)
    print(" LIBERTAS-BRIDGE v1.1")
    print("="*60)
    print("\nTippe 'exit' zum Beenden\n")
    
    while True:
        try:
            cmd = input(">>> ").strip()
            if cmd.lower() == 'exit':
                break
            comp = int(input("Komplexität (1-10): "))
            result = shield.route(comp, cmd)
            print(f"→ {result}\n")
        except Exception as e:
            print(f"Fehler: {e}\n")

if __name__ == "__main__":
    main()
