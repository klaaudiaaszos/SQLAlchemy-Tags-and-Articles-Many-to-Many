from sqlalchemy import String, Column, Integer, create_engine, ForeignKey, Table
from sqlalchemy.orm import declarative_base, Session, relationship, joinedload
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URL")
engine = create_engine (DATABASE_URI)
Base = declarative_base ()

article_tags = Table ('article_tags', Base.metadata,
                      Column ('article_id', Integer, ForeignKey ('articles.id'), primary_key= True),
                      Column ('tag_id', Integer, ForeignKey ('tags.id'), primary_key= True))

class Article (Base):
    __tablename__ = 'articles'
    id = Column (Integer, primary_key= True)
    title = Column (String, nullable= False)
    content = Column (String)
    tags = relationship ('Tag', secondary = article_tags, back_populates = 'articles')

class Tag (Base):
    __tablename__ = 'tags'
    id = Column (Integer, primary_key= True)
    name = Column (String, nullable= False)
    articles = relationship ('Article', secondary= article_tags, back_populates= 'tags')

Base.metadata.create_all (engine)

def add_article_with_tags (title, content, tag_names):
    with Session (engine) as session:
        article = Article (title = title, content = content)
        session.add (article)
        for tag_name in tag_names:
            tag = session.query(Tag).filter_by(name = tag_name).first()
            if not tag:
                tag = Tag (name = tag_name)
            article.tags.append (tag)
        session.commit ()

def get_all_articles ():
    with Session (engine) as session:
        articles = session.query (Article).options(joinedload(Article.tags)).all ()
        return articles
    
def add_tag_if_not_exist (tag_names):
    with Session (engine) as session:
        for tag_name in tag_names:
            if not session.query(Tag).filter_by(name=tag_name).first():
                new_tag = Tag (name = tag_name)
                session.add (new_tag)
        session.commit ()

add_tag_if_not_exist (['Python', 'SQL', 'Advanced'])
add_article_with_tags ("SQLAlchemy", "Learn SQLAlchemy", ['SQL', 'Python', 'Learn'])
add_article_with_tags ("Advanced SQLAlchemy", "Deep dive into ORM", ['SQL', 'Python', 'Advanced'])

articles = get_all_articles ()
for article in articles:
    tag_names = [tag.name for tag in article.tags]
    print (f"Artykul: {article.title}, tagi: {tag_names}")
            