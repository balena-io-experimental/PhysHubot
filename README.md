# [Hubot, a Physical Manifestation](https://github.com/resin-io-playground/PhysHubot)

![A robot head with glowing letters in its mouth](https://raw.githubusercontent.com/resin-io-playground/PhysHubot/master/img/finished.jpg)

Recently all Resineers came together in a single place for our annual summit, and there were several jokes about
whether Hubot, our virtual PA, would be joining us. I decided to spend a few quick minutes piping what Hubot says on
our chat service ([flowdock](https://www.flowdock.com)) to an
[LED grid](https://shop.pimoroni.com/collections/raspberry-pi/products/scroll-bot-pi-zero-w-project-kit). At this point
a wiser head than mine would point out certain truths about "a few quick minutes" but this, dear reader, is where my
learning journey began.

## tl,dr; or "the crux of the problem"

* The [npm (ie JS and compatibles) version of the SDK for Flowdock](https://www.npmjs.com/package/flowdock) is good.
* The [pip (ie Python) version of the SDK for the Scroll pHAT](https://github.com/pimoroni/scroll-phat-hd) is good.
* I created an internal webserver in Python that receives payloads from a Flowdock listener,
[PhysHubot](https://github.com/resin-io-playground/PhysHubot).
* Edit: I'm sure better, and easier, options do exist, but this seemed the most achievable with my knowledge.  I'd
especially choose this moment to call out [PyFlowdock](https://github.com/Aeron/PyFlowdock) which I wish I'd discovered
earlier.

## What I used

* [Scroll Bot Kit](https://shop.pimoroni.com/collections/raspberry-pi-zero/products/scroll-bot-pi-zero-w-project-kit) -
a quick note here.  The project uses the pins as the only mechanical connection holding the RPi in place.  I'm
not sure if there's a better way, but it is certainly on my ponder list.
* [A Flowdock instance](https://www.flowdock.com) - other chat services do exist, resin.io happen to use this one.
* Optional, a USB power bank.

## The journey begins

1) **Bright eyed and bushy tailed I set out.** Loads of my other work integrates using the Flowdock SDK, which is
published on npm. So I went looking for Scroll pHat support within nodeJS.  A quick search found a
[WIP library](https://github.com/alexellis/scroll-phat-node) but at this stage I knew I wanted scrolling text, and that
library marks scrolling text as a todo.
2) **If Scroll pHat will not come to JS, Flowdock will come to Python.** With JS out of the equation for
supporting the Scroll pHat I took a quick look around for Python libraries that would help me with Flowdock. *Probably
too quick as it turns out, but that's for 'next steps'.* I knew that I wanted to register a handler against their web
stream, which eliminated a couple of options, and I also did not care about posting to their endpoints. 
3) **I slept on it.** I'm often quite surprised by how much pondering my brain does while sleeping, and I'd love to
skim-read a scholarly article on this. I went to sleep with the bits that would solve the problem, even though I did
not realise it at the time, and woke with an idea.
4) **Just execute both.** I realised that I knew how to listen to Flowdock in NodeJS, I knew how to send web requests
from NodeJS, I knew how to listen to web requests in Python and I had a library to control the Scroll pHat in Python.
This made a complete chain from Flowdock to Scroll pHat.
5) **Wrestle with Docker a bit.** Getting the execution environment to manage both `npm install` and `pip install` took
a little learning, that I'm sure others would have just done in five minutes. In the end I went from our node base
image (because `apt-get python` had less setup than node). For future similar projects I'm likely to just start from
the dockerfile.template from this repository. It installs a bunch of stuff from apt-get, a couple of things from npm
and a couple of things from pip, before executing a
[shell script](https://github.com/resin-io-playground/PhysHubot/blob/master/src/flowdock_to_led.sh) that creates the
Python web server as a background task and also the flowdock listener. 
    * **Use `apt-get python-numpy`**, no **seriously**. The compile time on `python-numpy` if it gets bought in as a
    pip dependency is approximately forever.
6) **Long execution vs web requests.** The scrolling of text across the screen required a relatively long execution
time, but it was best if the web request resolved relatively rapidly. This lead to the LedManager class in
[http_to_led](https://github.com/resin-io-playground/PhysHubot/blob/master/src/flowdock_to_led.sh), which uses a thread
to manage the scrolling and holds a queue of messages to allow the web request to return promptly.
7) **Funky screen-saver.** The Scroll pHat library had a couple of cool example projects, and I decided that in-between
the marquee text the screen should display a pattern, to confirm things are powered up. A bit of interesting maths with
sine curves, pythagoras and a time-based offset and I had a ripple effect.
8) **Summit!** So, packed carefully in a lunchbox and full of expectations PhysHubot went to summit. I mostly left
PhysHubot alone, I hope that Hubot isn't the jealous sort, because, well there was
[this Beast v3](https://www.youtube.com/watch?v=SwIXXS2lQaU) tile that I really wanted to put some code on.

## Next steps

* Bring it all onto one language and one process. PyFlowdock, this is where you come in.
* Mount the RPi Zero W in a manner that won't impose mechanical wear on the pins.
