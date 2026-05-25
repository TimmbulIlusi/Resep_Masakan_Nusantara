from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecipeRecommender:

    def __init__(self, df):

        self.df = df

        self.vectorizer = TfidfVectorizer()

        self.tfidf_matrix = self.vectorizer.fit_transform(
            df['cleaned_ingredients']
        )

    def recommend(self, user_input):

        user_input = user_input.lower()

        input_words = []

        for item in user_input.split(","):

            words = item.strip().split()

            for word in words:

                input_words.append(word)

        # =========================
        # FILTER RESEP
        # =========================

        filtered_df = self.df[
            self.df['cleaned_ingredients'].apply(
                lambda x: any(
                    word in x
                    for word in input_words
                )
            )
        ]

        # =========================

        if filtered_df.empty:

            filtered_df = self.df

        filtered_matrix = self.vectorizer.transform(
            filtered_df['cleaned_ingredients']
        )

        user_vector = self.vectorizer.transform(
            [user_input]
        )

        similarity = cosine_similarity(
            user_vector,
            filtered_matrix
        )

        similarity_scores = similarity.flatten()

        filtered_df = filtered_df.copy()

        filtered_df['similarity'] = similarity_scores

        recommendations = filtered_df.sort_values(
            by='similarity',
            ascending=False
        )

        return recommendations.head(10)