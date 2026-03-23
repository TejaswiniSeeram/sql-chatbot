from semantic_router import Route
from semantic_router.routers import SemanticRouter
from semantic_router.encoders import FastEmbedEncoder

encoder = FastEmbedEncoder()

faq = Route(
    name="faq",
    utterances=[
        "How long does delivery take?",
        "Is there a loyalty or rewards program?",
        "what is your return policy?",
        "do you accept UPI payments?",
        "What happens if a book I ordered is out of stock?",
        "How do I contact customer support?",
    ]
)

sql = Route(
    name="sql",
    utterances=[
        "which artist has the most albums?",
        "show me all tracks in the rock genre",
        "What is the best selling track?",
        "Which customer has spent the most money?",
        "How many customers are from USA?",
    ]
)

router = SemanticRouter(routes=[faq, sql], encoder=encoder, auto_sync="local")
