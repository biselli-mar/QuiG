MAP_PROMPT_TEMPLATE = """Im Folgenden befindet sich eine Reihe von Dokumenten:

                        {text}
                        
                        Bitte identifiziere anhand der Liste von Dokumenten die Hauptthemen und wichtige Details.
                        Achte darauf, Beispiele und Definitionen wortgetreu zu übernehmen.
                        
                        Hilfreiche Antwort:"""

REDUCE_PROMPT_TEMPLATE = """Im Folgenden befindet sich eine Reihe von Zusammenfassungen:

                            {text}
                            
                            Nutze die Zusammenfassungen, um sie zu einer endgültigen, 
                            alles umfassenden Zusammenfassung zu kombinieren.
                            
                            Hilfreiche Antwort:"""

GENERATE_QUERY = """Generiere {num_questions} Quizfragen aus dem folgenden Text:
                    
                    {text}"""
