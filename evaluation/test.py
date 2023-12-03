import spacy

nlp = spacy.load("en_core_web_sm")

texto1 = """Having stayed in four other hotels in the French Quarter over the years during Jazzfest this is the only hotel I'd go back too. This hotel is in the Central Business District about a ten minute safe walk from the Quarter. Courteous helpful staff, clean and very nice room and hotel. Avoid the craziness and noise of some of the hotels in quarter and stay here. Also closer to the Garden District."""

texto2 = """The Drury Inn and Suites in the Central Business District, New Orleans is close to everything, a few minutes walk you are in the French Quarter or at the Superdome. Surrounded by restaurants and bars it makes it convenient for short or long term stays. The staff makes you feel right at home from the minute you walk in and the evening social is a great time to meet new people while enjoying the free perks the hotel offers."""

doc1 = nlp(texto1)
doc2 = nlp(texto2)

similaridade = doc1.similarity(doc2)

print(f"A pontuação de similaridade é: {similaridade}")