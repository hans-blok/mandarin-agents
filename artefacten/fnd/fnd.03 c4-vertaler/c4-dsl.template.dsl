// C4 DSL-template voor architectuurmodellen
// Vul de relevante secties aan op basis van input

workspace "<Naam van het systeem>" {
    model {
        // Personen
        person "<Naam persoon>" as <id>
        // Systemen
        system "<Naam systeem>" as <id>
        // Containers
        container "<Naam container>" as <id> "<Beschrijving>" "<Technologie>"
        // Componenten
        component "<Naam component>" as <id> "<Beschrijving>" "<Technologie>"
        // Relaties
        <bron> -> <doel> : "<relatie>"
    }
    views {
        // Context view
        systemContext <id> {
            include *
            autolayout lr
        }
        // Container view
        container <id> {
            include *
            autolayout lr
        }
        // Component view
        component <id> {
            include *
            autolayout lr
        }
    }
}
