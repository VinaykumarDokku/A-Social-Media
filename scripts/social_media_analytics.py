"""Analyze engagement metrics for social media posts."""

import csv
import argparse


def analyze_posts(csv_path):
    posts = []

    with open(csv_path, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        required = {"post_id", "likes", "comments", "shares", "views"}

        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"CSV must contain: {', '.join(sorted(required))}")

        for row in reader:
            post_id = row["post_id"].strip()

            if not post_id:
                raise ValueError("Post ID cannot be empty")

            try:
                likes = int(row["likes"])
                comments = int(row["comments"])
                shares = int(row["shares"])
                views = int(row["views"])
            except (ValueError, TypeError):
                raise ValueError(f"Invalid metrics for post {post_id}")

            if min(likes, comments, shares, views) < 0:
                raise ValueError("Metrics cannot be negative")

            engagement = likes + comments + shares
            engagement_rate = (
                engagement / views * 100 if views > 0 else 0
            )

            posts.append({
                "post_id": post_id,
                "likes": likes,
                "comments": comments,
                "shares": shares,
                "views": views,
                "engagement": engagement,
                "engagement_rate": engagement_rate,
            })

    return posts


def main():
    parser = argparse.ArgumentParser(
        description="Analyze social media engagement"
    )
    parser.add_argument("csv_file")
    args = parser.parse_args()

    posts = analyze_posts(args.csv_file)

    if not posts:
        print("No posts found")
        return

    total_likes = sum(post["likes"] for post in posts)
    total_comments = sum(post["comments"] for post in posts)
    total_shares = sum(post["shares"] for post in posts)
    total_views = sum(post["views"] for post in posts)

    total_engagement = total_likes + total_comments + total_shares

    overall_rate = (
        total_engagement / total_views * 100
        if total_views > 0 else 0
    )

    top_post = max(posts, key=lambda post: post["engagement"])

    print(f"Total posts: {len(posts)}")
    print(f"Total likes: {total_likes}")
    print(f"Total comments: {total_comments}")
    print(f"Total shares: {total_shares}")
    print(f"Overall engagement rate: {overall_rate:.2f}%")
    print(f"Top post by engagement: {top_post['post_id']}")


if __name__ == "__main__":
    main()
