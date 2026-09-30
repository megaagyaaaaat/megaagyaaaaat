#!/usr/bin/env python3

import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone

LOGIN = os.environ["GH_LOGIN"]
TOKEN = os.environ["GITHUB_TOKEN"]


def graphql(query, variables):
    body = json.dumps({
        "query": query,
        "variables": variables,
    }).encode()

    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Authorization": f"bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "github-profile-generator",
        },
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        result = json.load(response)

    if "errors" in result:
        raise RuntimeError(result["errors"])

    return result["data"]


def main():
    # Pin the window to whole UTC days.
    today = datetime.now(timezone.utc).date()

    from_dt = datetime.combine(
        today - timedelta(days=364),
        datetime.min.time(),
        tzinfo=timezone.utc,
    )

    to_dt = datetime.combine(
        today,
        datetime.max.time().replace(microsecond=0),
        tzinfo=timezone.utc,
    )

    query = """
    query(
      $login: String!
      $from: DateTime!
      $to: DateTime!
    ) {
      user(login: $login) {
        login

        contributionsCollection(
          from: $from
          to: $to
        ) {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }

          totalCommitContributions
          totalIssueContributions
          totalPullRequestContributions
          totalPullRequestReviewContributions
        }

        repositories(
          first: 100
          privacy: PUBLIC
          ownerAffiliations: OWNER
          isFork: false
          orderBy: {
            field: UPDATED_AT
            direction: DESC
          }
        ) {
          nodes {
            nameWithOwner
            primaryLanguage {
              name
            }
          }
        }
      }
    }
    """

    data = graphql(
        query,
        {
            "login": LOGIN,
            "from": from_dt.isoformat().replace("+00:00", "Z"),
            "to": to_dt.isoformat().replace("+00:00", "Z"),
        },
    )

    user = data["user"]

    if user is None:
        raise SystemExit(f"GitHub user not found: {LOGIN}")

    collection = user["contributionsCollection"]
    calendar = collection["contributionCalendar"]

    days = []

    for week in calendar["weeks"]:
        for day in week["contributionDays"]:
            days.append({
                "date": day["date"],
                "count": day["contributionCount"],
            })

    public_languages = {}

    for repo in user["repositories"]["nodes"]:
        language = repo["primaryLanguage"]

        if language is not None:
            name = language["name"]
            public_languages[name] = public_languages.get(name, 0) + 1

    stats = {
        "login": user["login"],
        "from": from_dt.isoformat(),
        "to": to_dt.isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_contributions": calendar["totalContributions"],
        "commits": collection["totalCommitContributions"],
        "issues": collection["totalIssueContributions"],
        "pull_requests": collection["totalPullRequestContributions"],
        "reviews": collection["totalPullRequestReviewContributions"],
        "days": days,
        "public_languages": public_languages,
    }

    with open("stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    print(
        f"Generated stats for {LOGIN}: "
        f"{calendar['totalContributions']} contributions"
    )
    print(
        f"UTC window: "
        f"{from_dt.isoformat()} → {to_dt.isoformat()}"
    )


if __name__ == "__main__":
    main()
