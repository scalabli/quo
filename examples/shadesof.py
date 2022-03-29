from quo import print

content = "           "
colors = (
        'bg:7fffd4',
        'bg:6ad0ad',
        'bg:55a288',
        'bg:417764'
        )

for color in colors:
    print(f"<style bg={colors}>{content}</style>")

print(f"<style bg='#6ad0ad'>{content}</style>")
print(f"<style bg='#55a288'>{content}</style>")
print(f"<style bg='#417764'>{content}</style>")
