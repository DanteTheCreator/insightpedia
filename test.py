async def analyze_topic(topic):
    try:
        article = await get_article(topic)
        if article:
            print("Topic already exists in the database!")
        else:
            article = page(topic) or page(suggest(topic))

            analyzer = ContentAnalyzer()
            summary = analyzer.summary(article.content)
            themes = analyzer.key_themes(article.content)
            trends = analyzer.trends(article.content)
            insights = analyzer.insights(article.content)

            new_entry_article = WikipediaAnalyzedData(
                title=article.title,
                summary=summary,
                themes=themes,
                trends=trends,
                insights=insights,
            )
            await create_article(new_entry_article)

    except HTTPException as e:
        print(f"Error: {e.detail}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

