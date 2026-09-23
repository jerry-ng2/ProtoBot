# Encodes SKILL.md Step 3 eligibility and Step 4 stale-status rules
# into the Step 5 proposal shape. Requires $milestoneMode and
# $activeMilestones.
if $milestoneMode != "active" and $milestoneMode != "none" then
  error("invalid milestone mode")
else
  . as $root
  | {
      milestone_mode: $milestoneMode,
      move_to_ready: [
        $root.items[]
        | select(
            .status == "Backlog"
            and .open_blocker_count == 0
            and .blockers_complete == true
            and .state == "OPEN"
            and .author_login != null
            and .author_login != "renovate[bot]"
            and .title != "Renovate Dependency Dashboard"
            and (
              if $milestoneMode == "none" then
                .milestone_number == null
              else
                .milestone_number != null
                and .milestone_state == "OPEN"
                and (.milestone_number as $n
                  | $activeMilestones
                  | any(.[]; .number == $n))
              end
            )
          )
        | {
            number,
            title,
            milestone,
            reason: (if $milestoneMode == "none" then
              "unblocked Backlog item with no milestone"
            else
              "unblocked Backlog item with an open milestone"
            end)
          }
      ] | sort_by(.number),
      stale_statuses: [
        $root.items[]
        | if .state == "OPEN" and .blockers_complete == false then
            {
              number,
              title,
              status,
              suggested_status: null,
              reason: "blocker data is incomplete"
            }
          elif .state == "CLOSED" and .status != "Done" then
            {
              number,
              title,
              status,
              suggested_status: "Done",
              reason: "closed item is not Done"
            }
          elif .state == "OPEN"
            and .status == "In progress"
            and .open_blocker_count > 0
            and .blockers_complete == true
            and all(.blocked_by[]; .state == "OPEN") then
            {
              number,
              title,
              status,
              suggested_status: null,
              reason: "In progress with open blockers"
            }
          elif .state == "OPEN"
            and .status == "Ready"
            and .open_blocker_count > 0 then
            {
              number,
              title,
              status,
              suggested_status: "Backlog",
              reason: "Ready with open blockers"
            }
          else
            empty
          end
      ] | sort_by(.number),
      excluded_cross_repository: [
        $root.excluded_cross_repository[]
        | {number, title, repository_owner, repository_name}
      ],
      excluded_non_issue: $root.excluded_non_issue
    }
end
