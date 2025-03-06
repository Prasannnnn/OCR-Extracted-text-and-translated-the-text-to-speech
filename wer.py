from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Input text for the word cloud
text = """"Whatever you do, do it 100%. When you work, work. When you laugh, laugh. When you eat, eat like it's your last meal."""

# Generate the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Save the word cloud to a file
wordcloud.to_file("wordcloud.png")

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
