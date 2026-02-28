Feature: {Feature Naam}
  As a {rol}
  I want {doel}
  So that {waarde}

  Background:
     Given {context die voor alle scenario's geldt, bijv. gebruiker ingelogd}
     And {extra conditie}

  Scenario: {Scenario 1 - Happy Path}
    Given {gebruiker bevindt zich op pagina X}
    And {data Y is beschikbaar}
    When {actie: gebruiker klikt op knop Z}
    Then {resultaat: systeem toont bericht A}
    And {data B is opgeslagen}

  Scenario: {Scenario 2 - Alternatief pad / Foutafhandeling}
    Given {conditie die leidt tot alternatief pad}
    When {actie}
    Then {verwacht resultaat: foutmelding of alternatieve flow}

  Scenario Outline: {Datagedreven test - Parameterisatie}
    Given {gebruiker voert <input> in veld}
    When {gebruiker bevestigt}
    Then {systeem toont resultaat <output>}

    Examples:
      | input | output |
      | 10    | 100    |
      | 20    | 200    |
      | -1    | Error  |

  # Tags: @wip @regression @api @ui
  # Rule: {Business Rule Reference, e.g. BR-01}
